import polars as pl
import numpy as np
from sklearn.svm import SVC  # support vector machine classifier
from data_predictor.models import Models


# implement support vector machine model through the abstract model class
class SupportVectorMachine(Models):
    def __init__(self, svc, df_train, model_params):  # can implement here to overwrite the abstract class definition
        super().__init__(df_train, model_params)  # super creates a temp object of parent class Models -
        # for example if there were methods there we would not need to redefine them here, or
        # variables that get defined in the constructor - we will likely need this to save time later
        self.svc = svc

    def fit(cls):
        svc = SVC(kernel=cls.model_params['kernel'], C=cls.model_params['C'])
        X = cls.df_train
        y = cls.df_train.select(pl.col("radiant_win"))
        svc.fit()
        return SupportVectorMachine(svc=svc, df_train=cls.df_train, model_params=cls.model_params)


    def predict(self):
        svc.predict()

    def validation(self):



