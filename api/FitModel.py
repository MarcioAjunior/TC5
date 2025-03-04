from Db import DbManager
import pandas as pd
import numpy as np
from lightfm.data import Dataset
from lightfm import LightFM

class LightFMTrainer:
    
    @classmethod
    def get_data(cls, db_params, model, len_train = 10000):
        db = DbManager(dict_connection=db_params)
        with db.conn as conn:
            train_data = pd.read_sql(sql = f"""
                                    select 
                                        u.id "userId", 
                                        n.id "newsId",
                                        a.engagement "engagement_score",
                                        0 "pop_score",
                                        cast(n.data_publicacao as timestamp) "issued_timestamp",
                                        n.embedding news_embedding,
                                        u.embedding user_weighted_embedding  
                                    from 
                                        "access" a
                                        join users u on a.id_user = u.id
                                        join news n on a.id_news  = n.id
                                    order by 
                                        a.id desc
                                    limit {len_train}
            """, con=conn)
        train_data['issued_timestamp'] = pd.to_datetime(train_data['issued_timestamp'], utc=True, errors='coerce')
        train_data['user_encoded'] =  model.user_encoder.fit_transform(train_data['userId'])
        train_data['news_encoded'] =  model.news_encoder.fit_transform(train_data['newsId'])
        return train_data
    
    @classmethod
    def get_popularity(cls, train_data):
        
        popularity_counts = train_data['newsId'].value_counts().reset_index()
        popularity_counts.columns = ['newsId', 'popularity_score']
        
        train_data = train_data.merge(
            popularity_counts, on='newsId', how='left'
        )
        return train_data
    
    @classmethod
    def normalize_data(cls, train_data, model):
        
        train_data['popularity_score'] = model.scaler_popularity.fit_transform(train_data[['popularity_score']])
        train_data['issued_timestamp'] = model.scaler_recency.fit_transform(train_data[['issued_timestamp']])

        return train_data

    @classmethod
    def create_interactions_features(cls, train_data, model):    
        user_embeddings_train = {row['user_encoded']: np.array(row['user_weighted_embedding']) for _, row in train_data.iterrows()}
        news_embeddings_train = {row['news_encoded']: np.array(row['news_embedding']) for _, row in train_data.iterrows()}
        
        num_users_train = len(train_data['user_encoded'])
        num_news_train = len(train_data['news_encoded'])
        
        embedding_dim_users_train = len(next(iter(user_embeddings_train.values())))
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
        
        (interactions_train, wheights_train) = dataset.build_interactions(
            [(row['user_encoded'], row['news_encoded'], row['engagement_score']) for _, row in train_data.iterrows()]
        )
        
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
        
        user_features_train = dataset.build_user_features(
            [
                (user_id, {f"emb_{i}": value for i, value in enumerate(embedding_avg)})
                for user_id, embedding_avg in user_embeddings_train.items()
            ],
            normalize=False
        )
        
        model.interactions = interactions_train
        model.wheights = wheights_train
        model.user_features = user_features_train
        model.item_features = item_features_train
        
        model.fit(
            interactions_train,
            user_features=user_features_train,
            item_features=item_features_train,
            num_threads=1,
            verbose=True,
            epochs=10
        )
        

    @classmethod
    def execute_pipeline(cls, model, db_params, len_train, epochs_train=10, num_threads=1):
        train_data = LightFMTrainer.get_data(db_params, model ,len_train)
        if len(train_data) > 10:
            print('-'*50)
            train_data = LightFMTrainer.get_popularity(train_data)
            print('-'*50)
            train_data = LightFMTrainer.normalize_data(train_data, model)
            print('-'*50)
            LightFMTrainer.create_interactions_features(train_data, model)

        return True