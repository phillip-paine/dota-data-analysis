"""Gradient Boosted Model for radiant win classifier"""
import polars as pl
import lightgbm as lgb

from data_predictor.models import Model

class LightGBM(Model):
    display_name = "GBM"
    def __init__(self, lgbm, df_train, params):
        super().__init__(df_train, model_params):

        self.lgbm = lgbm
        self.data = df_train
        self.params = params

    @classmethod
    def fit(cls, train_data, model_params):
        lgbm = lgb.LGBMClassifier()
        X = cls.df_train
        y = cls.df_train.select(pl.col("radiant_win"))
        lgbm.fit(X, y)
        return cls(lgbm=lgbm, df_train=df_train, params=params)

    def predict(self):
        self.lgbm.predict()

    def validation(self):
        lgbm = lgb.LGBMClassifier()
        X = cls.df_train
        y = cls.df_train.select(pl.col("radiant_win"))
        lgbm.fit(X, y)
        self.lgbm.predict()
        # TODO ; create validation accuracy dataframe

        # TODO : create plot object:

        return [lgbm, validation_accuracy]