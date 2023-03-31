"""prediction file for set of heroes for a match
This first attempt should allow us to enter 5v5 heroes and return a result prediction
"""
import polars as pl
from typing import Dict, List, Union
from data_formatter.utils import hero_name_from_id
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
    _radiant_heroes: List[Union[str, int]]
    _dire_heroes: List[Union[str, int]]

    @property  # use property as the getter - this is a decorator in python that is really the return getter method
    # if we wanted we could add e.g. a setter : @radiant_heroes.setter def radiant_heroes(self, val): self._ = ..
    def radiant_heroes(self):
        return self._radiant_heroes

    @property
    def dire_heroes(self):
        return self._dire_heroes


class MatchPrediction:
    def __init__(self, match: MatchRecord, model: str):
        # get teams:
        self.radiant = match.radiant_heroes
        self.dire = match.dire_heroes
        self.model_name = model
        self.loaded_model = self.load_model()
        self.df = pl.DataFrame
        # it might be easier to just write this as a json file and then use the function
        # create_public_matches_dataframe to get the match data
        # then pass that to th create_model_features function

        ## mayhbe delete this:
        radiant_teams = [type(a) for a in self.radiant]
        dire_teams = [type(b) for b in self.dire]
        if all(isinstance(r_, int) for r_ in radiant_teams) or all(isinstance(r_, str) for r_ in radiant_teams):
            self.radiant_teams_type = type(radiant_teams[0])
        else:
            raise ValueError('radiant team must be all integer or strings and be the same type')

        if all(isinstance(d_, int) for d_ in dire_teams) or all(isinstance(d_, str) for d_ in dire_teams):
            self.dire_teams_type = type(dire_teams[0])
        else:
            raise ValueError('dire team must be all integer or strings and be the same type')

    def load_model(self):
        """load appropriate model"""
        if self.model_name == "GBM":
            gbm_parameters_dict = {}
            gbm_model = GBM(GradientBoostingClassifier(), gbm_parameters_dict)
            saved_gbm_model_filename = "prod_fitted_gbm"
            gbm_model.load_model(f"data_predictor/{saved_gbm_model_filename}")
            return gbm_model
        elif self.model_name == "SVM":
            svc_parameters_dict = {'probability': True}
            # set probability=True in the constructor to use predict_proba function later
            svc_model = SupportVectorMachine(SVC(), svc_parameters_dict)
            saved_svc_model_filename = "prod_fitted_svc"
            svc_model.load_model(f"data_predictor/{saved_svc_model_filename}")
            return svc_model
        else:
            raise ValueError("Model must be one of GBM and SVM")
        return

    def create_feature_frame(self):
        # dont need this firt part now?:
        # run the data formatter code : turn hero id to name if necessary, i.e. if id are read in
        df_heroes = pl.DataFrame()
        hero_dict = get_hero_dict()
        if self.radiant_teams_type == int:
            df_heroes = hero_name_from_id(self.radiant, hero_dict, 'radiant')
        if self.dire_teams_type == int:
            df_heroes = hero_name_from_id(self.dire, hero_dict, 'dire')
        # still need this part:
        # then create the features from the modelling stage
        self.df = create_model_features(df_heroes)
        return self.df

    # return the winning team and their win percentage
    def predict_winner(self):
        # predict win % from loaded model:
        feature_columns = []
        predicted_df = self.loaded_model.predict(self.df[feature_columns])
        winning_team = "radiant" if predicted_df[f'yhat_{model_string}'] == 1 else "dire"
        winning_pct = predicted_df[f'yhat_{model_string}_probs'] if winning_team == "radiant" else \
            (1 - predicted_df[f'yhat_{model_string}_probs'])
        dict_winners = {'winning_side': winning_team, 'win_pct': winning_pct}
        return dict_winners

    # return the winning chance for radiant
    def predict(self):
        self.create_feature_frame()
        predicted_dict = self.predict_winner()
        return predicted_dict


if  __name__ == '__main__':
    model_string = "GBM"
    radiant_heroes_list = ['axe', 'bane', 'lina', 'ursa', 'zeus']
    dire_heroes_list = ['sven', 'dark seer', 'jakiro', 'luna', 'spectre']
    new_match = MatchRecord(radiant_heroes_list, dire_heroes_list)
    new_match_prediction = MatchPrediction(new_match, model_string)
    output = new_match_prediction.predict()
    print(output)
    a = 1
