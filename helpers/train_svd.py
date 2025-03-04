import pickle
import scipy.sparse
import pandas as pd
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer

PATH_SAMPLE = 'C:/Users/marci/OneDrive/Desktop/TC5/TC5/data'
PATH_HELPERS = 'C:/Users/marci/OneDrive/Desktop/TC5/TC5/helpers'

N_COMPONENTS = 50

news1 = pd.read_csv(f'{PATH_SAMPLE}/itens/itens/itens-parte1.csv')
news2 = pd.read_csv(f'{PATH_SAMPLE}/itens/itens/itens-parte2.csv')
news3 = pd.read_csv(f'{PATH_SAMPLE}/itens/itens/itens-parte3.csv')

df_news= pd.concat([news1, news2, news3], ignore_index=True)

textos_train = df_news['title']

with open(f"{PATH_HELPERS}/tfidf_vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)
    
tfidf_matrix = vectorizer.transform(textos_train)

svd = TruncatedSVD(n_components=N_COMPONENTS, random_state=42)
svd.fit(tfidf_matrix)

with open(f"{PATH_HELPERS}/svd_model.pkl", "wb") as f:
    pickle.dump(svd, f)