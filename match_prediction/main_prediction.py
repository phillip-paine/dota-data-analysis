"""prediction file for set of heroes for a match
This first attempt should allow us to enter 5v5 heroes and return a result prediction
"""
import polars as pl
import numpy as np
from typing import Dict, List, Union
from data_formatter.utils import hero_names_from_string_ints, hero_names_from_strings
from data_predictor.utils import create_model_features
from dataclasses import dataclass
from sklearn.ensemble import GradientBoostingClassifier
from data_predictor.gbm import GBM
from sklearn.svm import SVC
from data_predictor.svm import SupportVectorMachine
from data_formatter.utils import get_hero_dict


@dataclass(frozen=True) # frozen means that values cant be changed once constructor called
# this makes sense for us here because we dont want to teams to change after we give them
class MatchRecord:
    """Class for a match which is the set of radiant and dire heroes - should take either int or string form"""
    # note that _variable means that the variable is protected (i.e. not public member object) - like C++
    # @property (getter) and @variable.setter can be written to access them - like C++!
    _radiant_heroes: str
    _dire_heroes: str
    _avg_mmr: int

    @property  # use property as the getter - this is a decorator in python that is really the return getter method
    # if we wanted we could add e.g. a setter : @radiant_heroes.setter def radiant_heroes(self, val): self._ = ..
    def radiant_heroes(self):
        return self._radiant_heroes

    @property
    def dire_heroes(self):
        return self._dire_heroes

    @property
    def avg_mmr(self):
        return self._avg_mmr


class MatchPrediction:
    def __init__(self, match: MatchRecord, model: str):
        # get teams:
        self.radiant = match.radiant_heroes
        self.dire = match.dire_heroes
        self.avg_mmr = match.avg_mmr
        self.model_name = model
        self.model_reference = model.lower()
        self.loaded_model = self.load_model()
        self.df_heroes = pl.DataFrame({"radiant_team": self.radiant, "dire_team": self.dire})

        if all(isinstance(r_, int) for r_ in self.radiant) or all(isinstance(r_, str) for r_ in self.radiant):
            self.radiant_teams_type = type(self.radiant[0])
        else:
            raise ValueError('radiant team must be all integer or strings and be the same type')

        if all(isinstance(d_, int) for d_ in self.dire) or all(isinstance(d_, str) for d_ in self.dire):
            self.dire_teams_type = type(self.dire[0])
        else:
            raise ValueError('dire team must be all integer or strings and be the same type')

    def load_model(self):
        """load appropriate model"""
        if self.model_name == "GBM":
            gbm_parameters_dict = {}
            gbm_model = GBM(GradientBoostingClassifier(), gbm_parameters_dict)
            saved_gbm_model_filename = "TEST_fitted_gbm"
            gbm_model.load_model(f"data_predictor/{saved_gbm_model_filename}")
            return gbm_model
        elif self.model_name == "SVM":
            svc_parameters_dict = {'probability': True}
            # set probability=True in the constructor to use predict_proba function later
            svc_model = SupportVectorMachine(SVC(), svc_parameters_dict)
            saved_svc_model_filename = "TEST_fitted_svc"
            svc_model.load_model(f"data_predictor/{saved_svc_model_filename}")
            return svc_model
        else:
            raise ValueError("Model must be one of GBM and SVM")
        return

    def create_feature_frame(self):
        # dont need this firt part now?:
        # run the data formatter code : turn hero id to name if necessary, i.e. if id are read in

        hero_dict = get_hero_dict()
        if self.radiant_teams_type == int:
            self.df_heroes = hero_names_from_string_ints(self.df_heroes, hero_dict, 'radiant')
        else: # already checked string or int
            self.df_heroes = hero_names_from_strings(self.df_heroes, 'radiant')
        if self.dire_teams_type == int:
            self.df_heroes = hero_names_from_string_ints(self.df_heroes, hero_dict, 'dire')
        else:
            self.df_heroes = hero_names_from_strings(self.df_heroes, 'dire')
        # still need this part:
        # then create the features from the modelling stage
        df = create_model_features(self.df_heroes, prediction=True)
        # add mmr
        df = df.with_columns(pl.lit(self.avg_mmr).alias('avg_mmr'))
        return df

    # return the winning team and their win percentage
    def predict_winner(self, df):
        # predict win % from loaded model:
        x_pred = df.drop(["radiant_team", "dire_team", "radiant_heroes", "dire_heroes", "radiant_hero_1",
                          "radiant_hero_2", "radiant_hero_3", "radiant_hero_4", "radiant_hero_5", "dire_hero_1",
                          "dire_hero_2", "dire_hero_3", "dire_hero_4", "dire_hero_5"]).to_numpy()
        probability_prediction = np.array([p[0] for p in self.loaded_model.gbm.predict_proba(x_pred)])
        winning_team = "radiant" if probability_prediction > 0.5 else "dire"
        winning_pct = probability_prediction[0] if winning_team == "radiant" else \
            (100 - probability_prediction[0])
        dict_winners = {'winning_side': winning_team, 'win_pct': winning_pct}
        return dict_winners

    # return the winning chance for radiant
    def predict(self):
        df = self.create_feature_frame()
        predicted_dict = self.predict_winner(df)
        return predicted_dict


if __name__ == '__main__':
    model_string = "GBM"
    radiant_heroes_list = "Slark, Earthshaker, Shadow Fiend, Mars, Disruptor"
    dire_heroes_list = "Sven, Dark Seer, Jakiro, Luna, Spectre"
    avg_mmr = 3500
    new_match = MatchRecord(radiant_heroes_list, dire_heroes_list, avg_mmr)
    new_match_prediction = MatchPrediction(new_match, model_string)
    new_match_prediction.create_feature_frame()
    output = new_match_prediction.predict()
    print(output)
    a = 1
