import mlflow
from sklearn.neighbors import NearestNeighbors
from src.config import Config
from src.data_loader import DataLoader
import numpy as np


class RecommenderModel:
    def __init__(self, df):
        self.model = NearestNeighbors(n_neighbors=Config.KNN_K, algorithm=Config.ALGO, metric=Config.METRIC)
        mlflow.set_tracking_uri(Config.MLFLOW_TRACKING_URI)
        self.data = df
        self.movie_dict = {movie : index for index, movie in enumerate(list(self.data.index))}

    def train(self, data):
        self.model.fit(data)

        with mlflow.start_run() as run:
            mlflow.log_param('n_neighbors', Config.KNN_K)
            mlflow.log_param('metric', Config.METRIC)
            mlflow.sklearn.log_model(self.model, 'KNN_recommender_model')
            mlflow.register_model(f"runs:/{run.info.run_id}/KNN_recommender_model", "KNN_recommender_model")

            # mlflow.register_model("runs:/{run_id}/knn_recommender_model", "KNN_recommender_model")


    def predict(self, movie):
        if movie not in self.movie_dict:
            return f"Movie '{movie}' not found in the database."
        idx = self.movie_dict[movie]
        movie_vector = np.asarray([self.data.values[idx]])
        print(movie_vector.shape)
        distances, indices = self.model.kneighbors(movie_vector)

        movie_lists = list(self.data.index)
        movie_list = [movie_lists[indices[0][i]] for i in range(1, len(distances[0]))]

        return movie_list



if __name__ == '__main__':
    loader = DataLoader(Config.DATA_PATH) 
    data = loader.load_data()
    preprocessed_data, data = loader.preprocess(data)

    model = RecommenderModel(data)
    model.train(preprocessed_data)

    print(model.predict('101 Dalmatians (1996)'))
