
from flask import Flask, request, jsonify
import mlflow.sklearn
from src.config import Config
from src.data_loader import DataLoader

app = Flask(__name__)

class RecommenderAPI:
    def __init__(self):
        
        self.model = mlflow.sklearn.load_model("models:/KNN_recommender_model/latest")

        
        loader = DataLoader(Config.DATA_PATH)
        data = loader.load_data()
        self.preprocessed_data, self.data = loader.preprocess(data)
        self.movie_dict = {movie: index for index, movie in enumerate(list(self.data.index))}
        

    def predict(self, movie):
        
        if movie not in self.movie_dict:
            return f"Movie '{movie}' not found in the database."
        
        idx = self.movie_dict[movie]
        movie_vector = self.preprocessed_data[idx].reshape(1, -1)
        
        
        distances, indices = self.model.kneighbors(movie_vector)
        movie_list = [list(self.data.index)[indices[0][i]] for i in range(1, len(indices[0]))]

        return movie_list



recommender = RecommenderAPI()


@app.route('/recommend', methods=['POST'])
def recommend():
    data = request.json
    movie = data.get('movie')

    if not movie:
        return jsonify({'error': 'Please provide a movie name.'}), 400

    recommendations = recommender.predict(movie)
    return jsonify({'recommendations': recommendations})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)
