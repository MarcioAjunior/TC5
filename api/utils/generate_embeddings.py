import pickle
import os

PATH = os.path.dirname(os.path.abspath(__file__))

def load_models():
    """Carrega os modelos de TF-IDF e SVD a partir de pickles"""
    with open(f'{PATH}/tfidf_vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    with open(f'{PATH}/svd_model.pkl', 'rb') as f:
        svd = pickle.load(f)

    return vectorizer, svd

def get_embedding(texto):
    """Gera o embedding TF-IDF reduzido usando TruncatedSVD treinado."""
    vectorizer, svd = load_models()

    transformed_text = vectorizer.transform([texto])

    if transformed_text.shape[0] > 0:
        tfidf_reduced = svd.transform(transformed_text)
        return tfidf_reduced[0]
    
    return None
