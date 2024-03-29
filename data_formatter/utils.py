import pandas as pd
import polars as pl
import pickle
import json
import requests
from typing import Dict, Any


def get_hero_dict():
    file = open('data_scraper/data/hero_dict.pkl', 'rb')
    hero_dictionary = pickle.load(file)
    file.close()
    return hero_dictionary


def create_hero_feature_frame():
    req = requests.get(f'https://api.opendota.com/api/heroes')
    req_json = req.json()  # convert to json format
    # e.g. req_json[0] = {id, localized_name, primary_attr, attack_type, roles)
    # where roles is a list, e.g. [carry, escape, nuker]
    df = pd.json_normalize(req_json)
    df.drop(columns=['name', 'legs'], inplace=True)
    df.rename(columns={'localized_name': 'name'}, inplace=True)
    # role_list = list(set(df.roles.sum()))  # roles is a list column and sum will concatenate lists in each row
    df_roles = df['roles'].str.join(',').str.get_dummies(sep=',').astype(bool)
    df = pd.concat([df, df_roles], axis=1)
    df.to_pickle('data_storage/hero_feature_dataframe.pkl')
    return None


def create_hero_dataframe_features() -> None:
    df_hero_dict = pd.read_pickle('data_storage/hero_feature_dataframe.pkl')
    df_hero_dict = pl.from_pandas(df_hero_dict)
    # create agi, str and int category columns with polars: use get_dummies and cast to boolean
    df_hero_dict = pl.get_dummies(df_hero_dict, columns=['primary_attr']).with_columns(pl.col('^primary_attr.*$').cast(pl.Boolean))
    df_hero_dict.write_parquet('data_storage/formatted_hero_feature_dataframe.parquet')
    return None


def create_public_matches_datafame(json_records: dict) -> pd.DataFrame:
    # load hero dictionary:
    hero_dict = get_hero_dict()
    # write json to dataframe:
    df = pd.json_normalize(json_records)
    # # repeat for dire heroes:
    df = hero_names_from_id(df, hero_dict, "radiant")
    df = hero_names_from_id(df, hero_dict, "dire")
    return df


def hero_names_from_id(df_: pd.DataFrame, hero_dict_: Dict[str, Any], team: str) -> pd.DataFrame:
    df_[f'{team}_heroes'] = df_[f'{team}_team'].apply(lambda x: x.split(','))
    df_[[f'{team}1', f'{team}2', f'{team}3', f'{team}4', f'{team}5']] = df_[f'{team}_heroes'].to_list()
    df_[[f'{team}1', f'{team}2', f'{team}3', f'{team}4', f'{team}5']] = \
        df_[[f'{team}1', f'{team}2', f'{team}3', f'{team}4', f'{team}5']].astype(int)
    for i in range(1, 6):
        df_[f'{team}_hero_' + str(i)] = df_[f'{team}' + str(i)].apply(lambda x: hero_dict_[x])
    return df_


# these functions are different and assume the data has been entered as a comma separated string
# of hero names or the id as a string
def hero_names_from_strings(df_: pl.DataFrame, team: str) -> pl.DataFrame:
    df_ = df_.with_columns(pl.col([f'{team}_team']).apply(lambda x: x.split(', ')).alias(f'{team}_heroes'))
    # then unlist the column into 5 colummns:
    # suggested: explode -> pivot -> rename columns?
    df_ = df_.with_columns([
        df_[f'{team}_heroes'].apply(lambda x: x[0]).alias(f'{team}_hero_1'),
        df_[f'{team}_heroes'].apply(lambda x: x[1]).alias(f'{team}_hero_2'),
        df_[f'{team}_heroes'].apply(lambda x: x[2]).alias(f'{team}_hero_3'),
        df_[f'{team}_heroes'].apply(lambda x: x[3]).alias(f'{team}_hero_4'),
        df_[f'{team}_heroes'].apply(lambda x: x[4]).alias(f'{team}_hero_5')
    ])
    return df_


def hero_names_from_string_ints(df_: pl.DataFrame, team: str, hero_dict: Dict[str, Any]) -> pl.DataFrame:
    df_ = df_.with_columns(pl.col([f'{team}_team']).apply(lambda x: x.split(',').alias(f'{team}_heroes')))
    # then unlist the column into 5 colummns:
    # suggested: explode -> pivot -> rename columns?
    df_ = df_.with_columns([
        df_[f'{team}_heroes'].apply(lambda x: x[0]).alias(f'{team}_hero_1'),
        df_[f'{team}_heroes'].apply(lambda x: x[1]).alias(f'{team}_hero_2'),
        df_[f'{team}_heroes'].apply(lambda x: x[2]).alias(f'{team}_hero_3'),
        df_[f'{team}_heroes'].apply(lambda x: x[2]).alias(f'{team}_hero_4'),
        df_[f'{team}_heroes'].apply(lambda x: x[2]).alias(f'{team}_hero_5')
    ])
    # convert to int:
    df_[[f'{team}_hero_1', f'{team}_hero_2', f'{team}_hero_3', f'{team}_hero_4', f'{team}_hero_5']] = \
        df_[[f'{team}_hero_1', f'{team}_hero_2', f'{team}_hero_3', f'{team}_hero_4', f'{team}_hero_5']].apply(lambda x: x.cast(pl.Int64))
    # use hero dict to get string nme:
    for i in range(1, 6):
        df_[f'{team}_hero_' + str(i)] = df_[f'{team}' + str(i)].apply(lambda x: hero_dict[x])
    return df_


if __name__ == '__main__':
    # edit the working dir in the run/debug config page
    json_file = open('data_scraper/data/public_match_data_20230111_230019.json')
    records_json = json.load(json_file)
    df = create_public_matches_datafame(records_json)

    # create hero dictionary file:
    create_hero_feature_frame()
    create_hero_dataframe_features()