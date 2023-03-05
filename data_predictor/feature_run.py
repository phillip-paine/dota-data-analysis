"""Create the feature dataframe from the public match formatted dataframe"""
from data_predictor.utils import create_model_features, feature_processing
from run_constants.run_constants import TRAINING_MODEL_FILEPATH


def main_feature_run(filepath):
    df = create_model_features()
    # subset to columns for model fitting:
    df = df.drop(["lobby_type", "game_mode", "radiant_heroes", "dire_heroes", "radiant_hero_1",
                  "radiant_hero_2", "radiant_hero_3", "radiant_hero_4", "radiant_hero_5", "dire_hero_1",
                  "dire_hero_2", "dire_hero_3", "dire_hero_4", "dire_hero_5"])
    df = feature_processing(df)  # this is going to remove nulls for all columns
    df.write_parquet(filepath)


if __name__ == '__main__':
    filename = TRAINING_MODEL_FILEPATH
    main_feature_run(filename)
