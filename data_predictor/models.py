import polars as pl
import numpy as np
from abc import ABC, abstractmethod, ABCMeta  # abstract class
from typing import Dict, List, cast


# abstract class for models
class Method(ABCMeta, metaclass=ABCMeta):
    display_name: str

    def __str__(cls):
        return cls.display_name

    @abstractmethod
    def fit(cls, data, model_args) -> Model:
        raise NotImplementedError()


class Model(metaclass=Method):
    # initialise values
    def __init__(self, df_train, df_fit,  model_params):
        self.df_train = df_train
        self.df_fit = df_fit
        self.model_params = model_params

    @abstractmethod
    def predict(self, history_df: pl.DataFrame, future_df: pl.DataFrame):
        pass

    @abstractmethod
    def validation(self, history_train_df: pl.DataFrame, validation_df: pl.DataFrame):
        pass

    @property
    def method(self) -> Method:
        return cast(Method, type(self))

