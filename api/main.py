from fastapi import FastAPI
import dill
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from utils import generate_hashed_id, get_embedding
from FitModel import LightFMTrainer
from Db import DbManager
import threading
from utils import mix_recommendations, generate_random_name
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
import numpy as np


load_dotenv() 

PATH_UTILS = os.getenv("PATH_UTILS")
RECOMENDER_NAME = os.getenv("RECOMENDER_NAME")
DB_PARAMS = {
    "dbname" : os.getenv("DBNAME"),
    "user" : os.getenv("USER"),
    "password" : os.getenv("PASSWORD"),
    "host" : os.getenv("HOST"),
    "port" : os.getenv("PORT")
}

PATH_UTILS = os.path.dirname(os.path.abspath(__file__)) + '/utils'
db = DbManager(dict_connection=DB_PARAMS)

with open(f"{PATH_UTILS}/{RECOMENDER_NAME}", "rb") as f:
    custom_model =  dill.load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=['Access-Control-Allow-Origin']
)

class PredictionRequest(BaseModel):
    user_id: str
    use_heuristic: bool = False
    qtty_recommendations: int = 5
    
class UserRequest(BaseModel):
    nome: str
    
class NewsRequest(BaseModel):
    title: str
    subtitle: str = ''
    body: str = ''
    url: str = ''
    
class FitRequest(BaseModel):
    fit : bool
    len_train: int = 10000

class ReadRequest(BaseModel):
    user_id:str
    news_id: str

def run_training(model, db_params, len_train=10000):
    """Executa o treinamento em uma thread separada."""
    success = LightFMTrainer.execute_pipeline(model, db_params, len_train)
    model.state = 'ACTIVE'
    if success:
        print("Treinamento concluído com sucesso!")

@app.post("/predict")
async def predict(r: PredictionRequest): 
    """Faz uma predição para o usuário informado."""
    
    if custom_model.state == 'ACTIVE':
        if (r.user_id not in list(custom_model.user_encoder.classes_) or r.use_heuristic):
            
            ids_recomendation = [item for item in mix_recommendations(
                    list(custom_model.more_popularity),
                    list(custom_model.more_recency),
                    r.qtty_recommendations
                ) if item is not None]
            
            prediction = db.get_news(news_ids=ids_recomendation)
            return {"prediction": prediction}
            
        #Exploração
        if len(custom_model.more_recency) > 0 :
            predictions = [item for item in 
                            list(
                                custom_model.predict(r.user_id, list(custom_model.news_encoder.classes_),r.qtty_recommendations - 1)
                            ) + [custom_model.more_recency[0]] 
                    if item is not None]
        else:
            predictions = [item for item in
                            list(
                                custom_model.predict(r.user_id, list(custom_model.news_encoder.classes_),r.qtty_recommendations)
                            )
                    if item is not None]
        
        ids_recomendation = predictions[:r.qtty_recommendations]
        
        return {"prediction": db.get_news(news_ids=ids_recomendation)}
    
    return {"prediction": "Model is inactive"}

@app.post("/add_news")
async def add_news(r : NewsRequest):
    """Adiciona uma nova notícia ao modelo."""
    if custom_model.state == 'ACTIVE':
        news_id = generate_hashed_id(r.title)
        embedding = get_embedding(r.title)
            
        db.add_news(news_id, r.title, r.subtitle, r.body, r.url, embedding.tolist())
        training_thread = threading.Thread(target=run_training, args=(custom_model, DB_PARAMS))
        training_thread.start()
        
        custom_model.more_recency.appendleft(news_id)
        
        return {"news": news_id}
    return {"news": "Model is inactive"}

@app.post("/add_user")
async def add_user(r: UserRequest):
    """Adiciona um novo usuário ao modelo."""
    if custom_model.state == 'ACTIVE':
        user_id = generate_hashed_id(r.nome)
        embedding = [0] * 50
        
        db.add_user(user_id, r.nome, embedding)
        custom_model.news_users.appendleft(user_id)
        
        return {"user": user_id}
    
    return {"prediction": "Model is inactive"}

@app.post("/fit")
async def fit(r: FitRequest):
    """Retreina o modelo."""
    custom_model.state = 'INACTIVE'
    
    training_thread = threading.Thread(target=run_training, args=(custom_model, DB_PARAMS, r.len_train))
    training_thread.start()
    
    custom_model.state = 'ACTIVE'
    
    return {"stated": True}   

@app.post("/read_news")
def read_news(r : ReadRequest):
    """
    Cria ou atualiza o embedding do usuário com base em uma nova notícia acessada.
    """
    need_fit = True
    if custom_model.state == 'ACTIVE':
        
        news_embedding = db.get_news(news_id=r.news_id).get('embedding')
        user_embedding = db.get_user(user_id=r.user_id, users_ids=None).get('embedding')
    
        if news_embedding is None:
            raise HTTPException(status_code=404, detail="Embedding da notícia não encontrado")
    
        if r.user_id not in list(custom_model.user_encoder.classes_):
            #Usuario não encontrado, cria um novo usuário
            nome = generate_random_name()
            user_id = generate_hashed_id(nome)
            db.add_user(user_id, nome, [0] * 50)
            
        # gerando um exemplo de score de engajamento    
        engagement_score = (round(np.random.rand(), 6) / 100)
        
        if user_embedding == [0] * 50 or user_embedding is None:
            new_user_embedding = news_embedding
            access_id = db.make_access(
                user_id if user_embedding is None else r.user_id, 
                new_user_embedding, 
                engagement_score=engagement_score,
                news_id = r.news_id
            )
        else:
            new_user_embedding = (1 - engagement_score) * np.array(user_embedding) + engagement_score * np.array(news_embedding)
            access_id = db.make_access(
                r.user_id,
                new_user_embedding.tolist(),
                engagement_score=engagement_score,
                news_id = r.news_id
            )
            
        if need_fit:
            training_thread = threading.Thread(target=run_training, args=(custom_model, DB_PARAMS))
            training_thread.start()
        
        return {"read": access_id}
    
    return {"read": "Model is inactive"}

@app.get("/users")
async def users():
    """Retorna os últimos X usuários treinados."""
    
    list_user = list(custom_model.news_users)[-10:] + list(custom_model.user_encoder.classes_)[-12:]
        
    users_data = db.get_user(user_id=None ,users_ids=list_user)

    return {"users": users_data}


if __name__ == "__main__":
    import uvicorn
    import time
    time.sleep(8)
    uvicorn.run(app, host="0.0.0.0", port=8000)
