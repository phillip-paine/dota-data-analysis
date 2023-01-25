import pandas as pd
import numpy as np
import requests
import json


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


def create_model_features(df: pd.DataFrame):
    return df


if __name__ == '__main__':
    create_hero_feature_frame()
