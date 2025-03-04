
import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
from nltk.corpus import stopwords

nltk.download('stopwords')

PATH_SAMPLE = 'C:/Users/marci/OneDrive/Desktop/TC5/TC5/data'

stop_words = set(stopwords.words('portuguese'))

news1 = pd.read_csv(f'{PATH_SAMPLE}/itens/itens/itens-parte1.csv')
news2 = pd.read_csv(f'{PATH_SAMPLE}/itens/itens/itens-parte2.csv')
news3 = pd.read_csv(f'{PATH_SAMPLE}/itens/itens/itens-parte3.csv')

df_news= pd.concat([news1, news2, news3], ignore_index=True)

def remove_stopwords(texto):
    if isinstance(texto, str):
        palavras = texto.split()
        palavras_filtradas = [palavra for palavra in palavras if palavra.lower() not in stop_words]
        return " ".join(palavras_filtradas)
    return ""

df_news['title_clean'] = df_news['title'].apply(remove_stopwords)

vectorizer = TfidfVectorizer(min_df=2)

X = vectorizer.fit_transform(df_news['title_clean'])

with open('./TC5/helpers/tfidf_vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
