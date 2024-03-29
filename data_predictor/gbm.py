"""Gradient Boosted Model for radiant win classifier"""
import polars as pl
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from data_predictor.utils import model_evaluation, feature_processing
from data_predictor.models import Model
import pickle
from sklearn.model_selection import train_test_split


class GBM(Model):
    display_name = "GBM"

    def __init__(self, model, model_params):
        super().__init__(model_params)
        self.gbm = model

    @classmethod
    def fit(cls, train_data, model_params):
        gbm = GradientBoostingClassifier(**model_params)
        y = np.ravel(train_data.select(pl.col("radiant_win_flag")).to_numpy())
        X = train_data.drop(["radiant_win_flag", "radiant_win"]).to_numpy()
        gbm.fit(X, y)
        return cls(model=gbm, model_params=model_params)

    def predict_with_fitted(self, fitted_df: pl.DataFrame, predict_df: pl.DataFrame):
        fitted_df = fitted_df.with_columns(pl.lit(1).alias("history"))
        predict_df = predict_df.with_columns(pl.lit(0).alias("history"))
        complete_df = pl.concat([fitted_df, predict_df])
        return self.predict(complete_df)

    def predict(self, df: pl.DataFrame) -> pl.DataFrame:
        x_pred = df.drop(["radiant_win", "radiant_win_flag", "history"]).to_numpy()
        class_prediction = self.gbm.predict(x_pred)
        probability_prediction = np.array([p[0] for p in self.gbm.predict_proba(x_pred)])
        df = df.with_columns(pl.Series(name="yhat_gbm", values=class_prediction))  # pred class
        df = df.with_columns(pl.Series(name="yhat_gbm_probs", values=probability_prediction))  # pred class probabilities
        return df

    def validation(self, predicted_df: pl.DataFrame, roc_plot: bool = False):
        validation_data = predicted_df.filter(pl.col("history") == 0)  # only want unseen data here
        model_eval_dict = model_evaluation(validation_data['radiant_win_flag'], validation_data['yhat_gbm'],
                                           self.display_name, roc_plot)
        return model_eval_dict

    def fetch_model(self):
        return self.gbm

    def save_model(self, file):
        with open(file, 'wb') as pickle_file:
            pickle.dump(self.gbm, pickle_file)

    def load_model(self, file):
        with open(file, 'rb') as pickle_file:
            self.gbm = pickle.load(pickle_file)


if __name__ == '__main__':
    data = pl.read_parquet('data_storage/model_training_dataframe.parquet')
    data = data.drop(["lobby_type", "game_mode", "radiant_heroes", "dire_heroes", "radiant_hero_1",
                      "radiant_hero_2", "radiant_hero_3", "radiant_hero_4", "radiant_hero_5", "dire_hero_1",
                      "dire_hero_2", "dire_hero_3", "dire_hero_4", "dire_hero_5"])
    # drop_in_place only takes a string and not a list of strings?
    data = feature_processing(data)
    # data = data.lazy().drop_nulls().collect()
    train_data, test_data = train_test_split(data, test_size=0.2)
    gbm_parameters_dict = {}
    gbm_model = GBM(GradientBoostingClassifier(), gbm_parameters_dict)
    gbm_model = gbm_model.fit(train_data, gbm_parameters_dict)
    model_columns = train_data.drop(["radiant_win", "radiant_win_flag"]).columns
    df_feat_summary = pl.DataFrame({"names": model_columns, "imp": gbm_model.gbm.feature_importances_}).sort("imp", reverse=True)
    complete_data = gbm_model.predict_with_fitted(train_data, test_data)
    gbm_eval_metrics = gbm_model.validation(complete_data, True)
    print(gbm_eval_metrics['accuracy_score'])
    GBM_FILE_PATH = 'data_predictor/stored_models/TEST_fitted_gbm'
    gbm_model.save_model(GBM_FILE_PATH)
    gbm_model_2 = GBM(GradientBoostingClassifier(), gbm_parameters_dict)
    gbm_model_2.load_model(GBM_FILE_PATH)
