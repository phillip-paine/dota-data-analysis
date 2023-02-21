import polars as pl
import numpy as np
from data_predictor.models import Model
from typing import List, Dict, Any
from data_predictor.utils import read_data
from data_predictor.svm import SupportVectorMachine
from data_predictor.gbm import LightGBM
from run_constants.run_constants import MODELS_IN_USE, RUN_ARGUMENTS
from data_predictor.dataframe_holder import DataFrameHolder
from sklearn.svm import SVC
from lightgbm import LGBMClassifier


def run_models(models: List[str], model_arguments: Dict[str, Dict[Any, Any]], run_arguments: Dict[str, Any]) -> None:
    # create dataframe object for training and testing:
    data_holder = DataFrameHolder(read_data('model_training_dataframe.parquet'))
    for model in models:  # loop over any models entered
        # Create model object:
        try:
            assert model in MODELS_IN_USE
        except Exception as e:
            print(e, type(e))
            print(f'{model} must be one of {MODELS_IN_USE}')

        if model == "svm":
            model_inst = SupportVectorMachine(SVC(), data_holder, model_arguments['svm'])
        elif model == "gbm":
            model_inst = LightGBM(LGBMClassifier(), data_holder, model_arguments['gbm'])

        if run_arguments['validation_stage']:
            # train-test split for validation:
            model_inst.fit(data_holder.get_training_data())
            df_output = model_inst.predict(data_holder.get_training_data(), data_holder.get_testing_data())
            model_inst.validation(df_output.filter(pl.col('data_stage') == 'future'))

        # fit full model:
        model_inst.fit(data_holder.fetch_full_data())

        # save model to data store:
        model_inst.save_model(f"radiant_winrate_fitted_{model}")

    return None


if __name__ == '__main__':
    model_list = ['svm', 'gbm']
    svm_arguments = {}
    gbm_arguments = {}
    model_args = svm_arguments | gbm_arguments
    run_models(model_list, model_args, RUN_ARGUMENTS)
