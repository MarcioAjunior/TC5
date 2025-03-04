if __name__ == "__main__":
    from lightfm import LightFM
    from lightfm.data import Dataset
    from sklearn.preprocessing import MinMaxScaler
    from sklearn.preprocessing import LabelEncoder
    import cloudpickle as cp
    import pandas as pd
    import numpy as np
    from collections import deque

    
    
    class CustomLightFM:
        
        def __init__(self, loss="warp"):
            self.model = LightFM(
                loss=loss,
                item_alpha=1e-5,
                user_alpha=1e-5,
                random_state=42
            )

            self.user_encoder = LabelEncoder()
            self.news_encoder = LabelEncoder()

            self.scaler_popularity = MinMaxScaler()
            self.scaler_recency = MinMaxScaler()

            self.user_count = 0
            self.news_count = 0

            self.interactions = None
            self.weights = None

            self.user_features = None
            self.item_features = None

            self.more_popularity = None
            self.more_recency = deque(maxlen=10)

            self.state = 'ACTIVE'

        def fit(self, interactions, user_features=None, item_features=None, epochs=10, num_threads=1, verbose = True):
            """Treina o modelo com interações e features opcionais de usuários e itens."""
            print('RETREINANDO O MODELO') 
            self.model.fit(interactions, user_features=user_features, item_features=item_features, epochs=epochs, num_threads=num_threads, verbose = verbose)

            self.interactions = interactions

            return True

        def add_user(self, user_id):
            """Adiciona um novo usuário ao modelo."""
            print('ADICIONANDO USUARIO')
            if user_id in self.user_encoder.classes_:
                return self.user_encoder.transform([user_id])[0]

            self.user_encoder.classes_ = np.append(self.user_encoder.classes_, user_id)
            new_id = self.user_count
            self.user_count += 1
            return new_id

        def add_news(self, news_id):
            """Adiciona uma nova notícia ao modelo."""
            print('ADICIONANDO NOTICIA')
            if news_id in self.news_encoder.classes_:
                return self.news_encoder.transform([news_id])[0]

            self.news_encoder.classes_ = np.append(self.news_encoder.classes_, news_id)
            new_id = self.news_count
            self.news_count += 1
            return new_id

        def predict(self, user_id, news_ids, top_n=5) -> list:
            """Faz uma predição de recomendação para um usuário com base no ID externo."""
            try:
                user_internal = self.user_encoder.transform([user_id])[0]
                news_internal = self.news_encoder.transform(news_ids)

                user_array = np.full(len(news_internal), user_internal)

                scores = self.model.predict(user_array, news_internal)

                top_items = np.argsort(-scores)[:top_n]
                print('PREDIZENDO PARA O USUARIO')
                return list(self.news_encoder.inverse_transform(news_internal[top_items]))
            except Exception as e:
                print(e)
                print('RETORNANDO NOTICIAS POPULARES PARA O USUARIO')
                return self.more_popularity.values()
    
    model = CustomLightFM()
    
    PATH = '/home/lightfm/load_data/'
    PATH_MODEL = '/home/lightfm/'
    
    train_data_0 = pd.read_parquet(f'{PATH}chunk_0.parquet')
    train_data_1 = pd.read_parquet(f'{PATH}chunk_1.parquet')
    train_data_2 = pd.read_parquet(f'{PATH}chunk_2.parquet')
    train_data_3 = pd.read_parquet(f'{PATH}chunk_3.parquet')
    train_data_4 = pd.read_parquet(f'{PATH}chunk_4.parquet')
    train_data_5 = pd.read_parquet(f'{PATH}chunk_5.parquet')

    train_data = pd.concat([train_data_0, train_data_1, train_data_2, train_data_3, train_data_4, train_data_5], ignore_index=True)
    
    del train_data_0
    del train_data_1
    del train_data_2
    del train_data_3
    del train_data_4
    del train_data_5
    
    train_data['user_encoded'] =  model.user_encoder.fit_transform(train_data['userId'])
    train_data['news_encoded'] =  model.news_encoder.fit_transform(train_data['newsId'])
    
    train_data.sort_values(by='popularity_score', inplace=True, ascending=False)
    
    user_embeddings_train = {row['user_encoded']: np.array(row['user_weighted_embedding']) for _, row in train_data.iterrows()}
    news_embeddings_train = {row['news_encoded']: np.array(row['news_embedding']) for _, row in train_data.iterrows()}
    
    num_users_train = len(train_data['user_encoded'])
    embedding_dim_users_train = len(next(iter(user_embeddings_train.values())))
    
    num_news_train = len(train_data['news_encoded'])
    embedding_dim_news_train = len(next(iter(news_embeddings_train.values())))
    
    users_feature_matrix_train = np.zeros((num_users_train, embedding_dim_users_train))
    user_id_map_train = {user_id: i for i, user_id in enumerate(list(user_embeddings_train.keys()))}
    
    item_feature_matrix_train = np.zeros((num_news_train, embedding_dim_news_train))
    item_id_map_train = {news_id: i for i, news_id in enumerate(list(news_embeddings_train.keys()))}
    
    for user_id, embedding in user_embeddings_train.items():
        users_feature_matrix_train[user_id_map_train[user_id]] = embedding
        
    for news_id, embedding in news_embeddings_train.items():
        item_feature_matrix_train[item_id_map_train[news_id]] = embedding
        
    dataset = Dataset()
    dataset.fit(
        users=train_data['user_encoded'].unique(),
        user_features=[f"emb_{i}" for i in range(embedding_dim_news_train)],
        items=train_data['news_encoded'].unique(),
        item_features=[f"emb_{i}" for i in range(embedding_dim_news_train)] + ['recency'] + ['popularity'],
    )
    
    (interactions_train, wheights_train) = dataset.build_interactions([(row['user_encoded'], row['news_encoded'], row['engagement_score']) for _, row in train_data.iterrows()])
    
    model.interactions = interactions_train
    model.weights = wheights_train
    
    item_recency_train = {row['news_encoded']: row['issued_timestamp'] for _, row in train_data.iterrows()}
    item_popularity_train = {row['news_encoded']: row['popularity_score'] for _, row in train_data.iterrows()}
    
    item_features_train = dataset.build_item_features(
        [
            (news_id,
            {f"emb_{i}": value for i, value in enumerate(embedding)} |
            {"recency": item_recency_train[news_id]} |
            {"popularity": item_popularity_train[news_id]})
            for news_id, embedding in news_embeddings_train.items()
        ], normalize=False
    )
    
    model.item_features = item_features_train
    
    user_features_train = dataset.build_user_features(
        [
            (user_id, {f"emb_{i}": value for i, value in enumerate(embedding_avg)})
            for user_id, embedding_avg in user_embeddings_train.items()
        ],
        normalize=False
    )
    
    model.user_features = user_features_train
    
    model.fit(
        interactions_train,
        epochs=10,
        num_threads=2,
        item_features=item_features_train,
        user_features=user_features_train
    )
    
    top_news = train_data[['newsId', 'news_encoded', 'popularity_score']].head(10)
    top_news.reset_index(drop=True, inplace=True)
    
    more_popularity = dict().fromkeys(range(10))
    
    for i, item  in  top_news.iterrows():
        if item['newsId'] not in list(more_popularity.values()):
            more_popularity[i] = item['newsId']
        
    model.more_popularity = dict(more_popularity)
        
    try:
        with open(f'{PATH_MODEL}custom_model.pkl', 'wb') as file:
            cp.dump(model, file)
        print("Model saved successfully!")
    except Exception as e:
        print(f"Error saving model: {str(e)}")