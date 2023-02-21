"""Create the feature dataframe from the public match formatted dataframe"""
from data_predictor.utils import create_model_features
from run_constants.run_constants import TRAINING_MODEL_FILEPATH


def main_run(filepath):
    df = create_model_features()
    df.write_parquet(filepath)


if __name__ == '__main__':
    filename = TRAINING_MODEL_FILEPATH
    main_run(filename)
