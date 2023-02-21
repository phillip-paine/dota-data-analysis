"""constants needed in the project"""
from data_predictor.svm import SupportVectorMachine
from data_predictor.gbm import LightGBM

MODELS_IN_USE = ['svm', 'gbm']

RUN_ARGUMENTS = {'validation_stage': True}
TRAINING_MODEL_FILEPATH = 'data_storage/model_training_dataframe.parquet'