"""create dataframe from scraped json"""
from os import listdir
from os.path import isfile, join
import pandas as pd
import json
import pyarrow
from utils import create_public_matches_datafame


def run_main_formatter(save_filepath: str):
    # run the formatting functions:
    pathdir = 'data_scraper/data'
    files = [f for f in listdir(pathdir) if isfile(join(pathdir, f))]
    files = [f for f in files if f.startswith('public_match_data')]
    df_store = pd.DataFrame()
    for file in files:
        # with open() as .. is preferred becuase if we use open() by itself we need to use close() afterwards
        with open(pathdir+'/'+file, encoding='utf-8') as json_file:
            match_data_file = json.load(json_file)
        df_temp = create_public_matches_datafame(match_data_file)
        df_store = pd.concat([df_store, df_temp])
    df_store.to_parquet(save_filepath)


    return None


if __name__ == '__main__':
    # create dataframes from scraped data:
    PATH_TO_SAVE = 'data_storage/public_match_data_formatted.parquet'
    run_main_formatter(PATH_TO_SAVE)
