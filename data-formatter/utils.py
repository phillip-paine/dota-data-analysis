import pandas as pd
import pickle
import json


def get_hero_dict():
    file = open('data-scraper/data/hero_dict.pkl', 'rb')
    hero_dictionary = pickle.load(file)
    file.close()
    return hero_dictionary


def create_public_matches_datafame(json_records: dict):
    # load hero dictionary:
    hero_dict = get_hero_dict()
    # write json to dataframe:
    df = pd.json_normalize(json_records)
    # create radiant hero columns:
    df['radiant_heroes'] = df['radiant_team'].apply(lambda x : x.split(','))
    df[['radiant1', 'radiant2', 'radiant3', 'radiant4', 'radiant5']] = df['radiant_heroes'].to_list()
    df[['radiant1', 'radiant2', 'radiant3', 'radiant4', 'radiant5']] = \
        df[['radiant1', 'radiant2', 'radiant3', 'radiant4', 'radiant5']].astype(int)
    for i in range(1, 6):
        df['radiant_hero_' + str(i)] = df['radiant' + str(i)].apply(lambda x: hero_dict[x])
    # repeat for dire heroes:
    df['dire_heroes'] = df['dire_team'].apply(lambda x : x.split(','))
    df[['dire1', 'dire2', 'dire3', 'dire4', 'dire5']] = df['dire_heroes'].to_list()
    df[['dire1', 'dire2', 'dire3', 'dire4', 'dire5']] = \
        df[['dire1', 'dire2', 'dire3', 'dire4', 'dire5']].astype(int)
    for i in range(1, 6):
        df['dire_hero_' + str(i)] = df['dire' + str(i)].apply(lambda x: hero_dict[x])

    df.to_csv()
    return None


if __name__ == '__main__':
    # edit the working dir in the run/debug config page
    json_file = open('data-scraper/data/public_match_data_20230111_230019.json')
    records_json = json.load(json_file)
    create_public_matches_datafame(records_json)