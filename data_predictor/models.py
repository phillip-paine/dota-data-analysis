import polars as pl
import numpy as np
from abc import ABC, abstractmethod, ABCMeta  # abstract class
from typing import Dict, List, cast


# create metaclass for the model abstract class - metaclass allows us to define how a class is instantiated
# by default the metaclass is 'type' e.g. print(type(Class)) returns type: type
class Method(ABCMeta, metaclass=ABCMeta):
    display_name: str

    # call str magic method to create a string representation of the class - now if we print class it will
    # return display_name string instead of <__main__.Class <memory address>>
    def __str__(cls):
        return cls.display_name

    @abstractmethod
    def fit(cls, data, model_args):
        raise NotImplementedError()


class Model(metaclass=Method):
    # initialise values
    def __init__(self, model_params):
        self.model_params = model_params

    @abstractmethod
    def predict_with_fitted(self, history_df: pl.DataFrame, future_df: pl.DataFrame):
        pass

    @abstractmethod
    def predict(self, df: pl.DataFrame):
        pass

    @abstractmethod
    def validation(self, validation_df: pl.DataFrame, plot: bool):
        pass

    @abstractmethod
    def fetch_model(self):
        pass

    def save_model(self, file):
        pass

    @property
    def method(self) -> Method:
        return cast(Method, type(self))

