import polars as pl
import numpy as np
from data_predictor.models import Model
from typing import List, Dict, Any

def run_models(models: List[str], model_arguments: List[Dict[Any, Any]]) -> None:

    for model in models:  # loop over any models entered
        # Create model object:
        model_object = Model()
        # set radiant_win to y:

        # fit model:

        # validate fitted model:

        # predict future output:

        # save to data store:

    return None


if __name__ == '__main__':
    model_list = []
    run_models()
