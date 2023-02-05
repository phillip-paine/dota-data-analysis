import polars as pl
import numpy as np
from abc import ABC, abstractmethod  # abstract class

# abstract class for models
class Models(ABC):
    # initialise values
    def __init__(self, df_train, df_fit,  model_params):
        self.df_train = df_train
        self.df_fit = df_fit
        self.model_params = model_params

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass

    @abstractmethod
    def validation(self):
        pass

