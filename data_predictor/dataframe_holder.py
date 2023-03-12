import polars as pl
from sklearn.model_selection import train_test_split

class DataFrameHolder():
    def __init__(self, df):
        self.df = df
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None

    def preprocess(self):
        # set radiant_win to y:
        self.df.rename({'radiant_win': 'y'}, inplace=True)  # does it have inplace?

    def fetch_full_data(self):
        return self.df

    def create_train_test(self, test_prop: float = 0.2):
        df_train, df_test = train_test_split(self.df, test_size=test_prop, random_state=11, stratify=self.df['y'])
        self.y_train, self.y_test = df_train['y'], df_test['y']
        self.x_train, self.x_test = df_train.select(), df_test.select()

    def get_training_data(self):
        return {'features': self.x_train, 'y': self.y_train}

    def get_testing_data(self):
        return {'features': self.x_test, 'y': self.y_test}



