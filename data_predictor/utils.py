import pandas as pd
import polars as pl
import numpy as np
import json


def create_model_features():
    """main function to create model features from match data + hero feature"""
    # read data only useful columns
    df = pl.scan_parquet('data_storage/public_match_data_formatted.parquet').select([
        pl.col("avg_mmr"), pl.col("radiant_win"), pl.col("lobby_type"), pl.col("game_mode"),
        pl.col('^radiant_hero.*$'), pl.col('^dire_hero.*$')
    ]).filter((pl.col("lobby_type").is_in([0, 7])) & (pl.col("game_mode") == 22)).collect()
    # lobby type : 0 = normal (unranked), 7 = ranked mm
    # game mode: 22 = all pick, 4 = single draft (china likes draft?), 3 = random draft (china mostly)

    # add hero attributes: count each of the labels for radiant and dire and primary attributes and attack types
    df_hero_dict = pl.read_parquet('data_storage/formatted_hero_feature_dataframe.parquet')
    # 1. radiant and dire melee count:
    df = count_attribute_teams('Carry', df, df_hero_dict)
    df = count_attribute_teams('Support', df, df_hero_dict)
    df = count_attribute_teams('Durable', df, df_hero_dict)
    df = count_attribute_teams('primary_attr_agi', df, df_hero_dict)
    df = count_attribute_teams('primary_attr_str', df, df_hero_dict)
    df = count_attribute_teams('primary_attr_int', df, df_hero_dict)
    return df


def count_attribute_teams(attribute: str, df: pl.DataFrame, hero_dict: pl.DataFrame):
    teams = ['radiant', 'dire']
    for t_ in teams:
        # need an apply function with a look-up to the hero_dictionary
        # df = df.with_columns(pl.lit(0).alias(f'{t_}_{attribute}_count'))
        df = df.with_columns([
            pl.struct(pl.col(rf'^{t_}_hero_.*$')).
            # apply(lambda x: calculate_attribute_count(x, attribute, hero_dict)).
            apply(lambda row:
                    sum([int(hero_dict.filter(pl.col('name') == hero_).select(attribute)[0, 0])
                     for hero_ in list(row.values())])).
            alias(f'{t_}_{attribute}_count')
        ])

    return df

def model_evaluation():

    return None

def evaluation_metrics():

    return None

def evaluation_plots():

    return None


if __name__ == '__main__':
    # create_model_features()
    hold = 1
