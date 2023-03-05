import polars as pl
import numpy as np
from run_constants.run_constants import TRAINING_MODEL_FILEPATH
from sklearn.metrics.cluster import contingency_matrix
from sklearn import metrics
from typing import Dict, Any
import matplotlib.pyplot as plt


def create_model_features() -> pl.DataFrame:
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
    # 2. radiant win flag: need integer column for many models:
    df = df.with_column(pl.col("radiant_win").cast(pl.Int8).alias("radiant_win_flag"))  # checked.
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


def feature_processing(df: pl.DataFrame) -> pl.DataFrame:
    # 1. Deal with missing values in feature dataframe:
    df = df.lazy().drop_nulls().collect()
    # 2. Remove rows with missing values in classification column:
    return df


def compare_model_evaluations(y: pl.Series, yhat_dict: Dict[str, Any]):
    coef_dict = {}
    fig = plt.figure()
    for model_str, yhat in yhat_dict.items():
        coef_dict[model_str] = model_evaluation(y, yhat)
        # AUC with all models:
        fpr, tpr, thresholds = metrics.roc_curve(y, yhat, pos_label=2)
        fig = add_roc_curve_to_figure(fig, fpr, tpr)
    return coef_dict


def model_evaluation(y: pl.Series, yhat: pl.Series):
    # calculate the YPC (or MCC):
    ypc = metrics.matthews_corrcoef(y, yhat)  # yule's phi coefficient (also called Matthews correlation coef.)
    # area under ROC curve:
    fpr, tpr, _ = metrics.roc_curve(y, yhat, pos_label=2)
    roc_plot = plot_roc_figure(fpr, tpr)
    return ypc, roc_plot


def add_roc_curve_to_figure(fig_, fpr, tpr):
    auc_roc = metrics.auc(fpr, tpr)
    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % auc_roc)
    return fig_


def plot_roc_figure(fpr, tpr):
    auc_roc = metrics.auc(fpr, tpr)
    fig = plt.figure()
    plt.title('Receiver Operating Characteristic')
    plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % auc_roc)
    plt.legend(loc = 'lower right')
    plt.plot([0, 1], [0, 1],'r--')
    plt.xlim([0, 1])
    plt.ylim([0, 1])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    return fig


def read_data(file_name: str):
    extension = file_name.split('.')[-1]
    # python >=3.10 has match-case (like switch statement)
    try:
        assert extension in ['parquet', 'csv', 'json']  # check if filetype is one of this list with assert
    except Exception as e:
        print(e, type(e))
        print("Not a recognised filetype - should be one of parquet, csv and json")

    else:  # if try passes (and no exception encountered)
        if extension == 'parquet':
            return pl.read_parquet(file_name)
        elif extension == 'csv':
            return pl.read_csv(file_name)
        elif extension == 'json':
            return pl.read_json(file_name)


if __name__ == '__main__':
    df = create_model_features()
    df.write_parquet(TRAINING_MODEL_FILEPATH)
    hold = 1
