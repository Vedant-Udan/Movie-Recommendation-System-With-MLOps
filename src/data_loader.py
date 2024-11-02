import os
import pandas as pd
from scipy.sparse import csr_matrix
from abc import ABC, abstractmethod


class Dataset(ABC):
    @abstractmethod
    def load(self, file_path: str) -> pd.DataFrame:
        pass
    
class Stats(Dataset):
    def load(self, file_path: str) -> pd.DataFrame:

        files = os.listdir(file_path)
        info_file = [f for f in files if f.endswith('.info')]

        if len(info_file) == 0:
            raise ValueError('No info file present.')

        file_path = os.path.join(file_path, info_file[0])
        df = pd.read_csv(file_path, header=None)

        return df

class UserData(Dataset):
    def load(self, file_path: str) -> pd.DataFrame:

        files = os.listdir(file_path)
        data_file = [f for f in files if f.endswith('.data')]
        
        if len(data_file) == 0:
            raise ValueError('No data file is present')

        file_path = os.path.join(file_path, 'u.data')
        columns = ['user id','movie id','rating','timestamp']
        df = pd.read_csv(file_path, sep='\t', header= None, names = columns)
        
        return df

class ItemData(Dataset):
    def load(self, file_path: str) -> pd.DataFrame:

        files = os.listdir(file_path)
        data_file = [f for f in files if f.endswith('.item')]
        
        if len(data_file) == 0:
            raise ValueError('No item file is present')

        file_path = os.path.join(file_path, 'u.item')
        columns =['movie id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'] 
        df = pd.read_csv(file_path, sep='|', header= None, names = columns, encoding='latin-1')
        
        return df

    
class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.stats_loader = Stats()
        self.user_loader = UserData()
        self.item_loader = ItemData()

    def load_data(self) -> pd.DataFrame:
        """Loads and merges user, item, and stats data."""
        
        overall_stats = self.stats_loader.load(self.file_path)
        print("Details of users, items, and ratings in the dataset:", list(overall_stats[0]))

        user_data = self.user_loader.load(self.file_path)
        item_data = self.item_loader.load(self.file_path)
        
        movie_data = item_data[['movie id', 'movie title']]
        merged_data = pd.merge(user_data, movie_data, how='inner', on='movie id')

        refined_data = merged_data.groupby(['user id', 'movie title'], as_index=False).agg({'rating': 'mean'})
        
        return refined_data

    def preprocess(self, data):

        df = data.pivot(index='movie title', columns='user id', values='rating').fillna(0)
        sparse_df = csr_matrix(df.values)

        return sparse_df, df