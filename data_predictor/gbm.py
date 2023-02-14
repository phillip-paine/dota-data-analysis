"""Gradient Boosted Model for radiant win classifier"""
import polars as pl
import lightgbm as lgb
from data_predictor.utils import model_evaluation
from data_predictor.models import Model


class LightGBM(Model):
    display_name = "GBM"

    def __init__(self, model, df_train, model_params):
        super().__init__(df_train, model_params)
        self.lgbm = model
        self.data = df_train
        self.gbm_params = model_params

    @classmethod
    def fit(cls, train_data, model_params):
        lgbm = lgb.LGBMClassifier(model_params[''])
        X = cls.train_data
        y = cls.train_data.select(pl.col("radiant_win"))
        lgbm.fit(X, y)
        return cls(lgbm=lgbm, df_train=train_data, params=model_params)

    def predict(self, fitted_df: pl.DataFrame, predict_df: pl.DataFrame):
        complete_df = pl.concat([fitted_df, predict_df])
        self.lgbm.predict(complete_df)

    def validation(self, predicted_df: pl.DataFrame):
        model_evaluation(predicted_df['y'], predicted_df['yhat'])
        return None