from src.config import Config
from src.data_loader import DataLoader
from src.model import RecommenderModel


class TrainingPipeline:
    def __init__(self, file_path):
        self.loader = DataLoader(file_path)
        data = self.loader.load_data()
        self.preprocessed_data, data = self.loader.preprocess(data)
        self.model = RecommenderModel(data)

    def runs(self):

        self.model.train(self.preprocessed_data)
        print("Training completed")

if __name__ == '__main__':
    pipeline = TrainingPipeline(Config.DATA_PATH)
    pipeline.runs()
