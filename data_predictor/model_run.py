import polars as pl
import numpy as np
from data_predictor.models import Model
from typing import List, Dict, Any

def run_models(models: List[str], model_arguments: List[Dict[Any, Any]]) -> None:

    for model in models:  # loop over any models entered
        # Create model object:
        model_object = Model()
        # set radiant_win to y:

        # train-test split for validation:

        # fit model:

        # predict future output for test portion:

        # validate fitted model:

        # rebuild trained model on all data:

        # save to data store:

    return None


if __name__ == '__main__':
    model_list = []
    run_models()
