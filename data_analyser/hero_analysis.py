import pandas as pd
from data_formatter.utils import get_hero_dict
import pyarrow
import copy


def hero_winrate(save_filepath):
    filepath = 'data_storage/public_match_data_formatted.parquet'
    df_matches = pd.read_parquet(filepath)
    # Dataframe of heroes:
    hero_winrate_dict = {'hero': {'matches': 1, 'wins': 0}}
    for i in range(len(df_matches.index)):
        for r in range(1, 6):
            if hero_winrate_dict.get(df_matches.iloc[i][f'radiant_hero_{r}']):
                hero_winrate_dict[df_matches.iloc[i][f'radiant_hero_{r}']]['matches'] += 1
                hero_winrate_dict[df_matches.iloc[i][f'radiant_hero_{r}']]['wins'] += \
                    int(df_matches.iloc[i]['radiant_win'])
            else:
                hero_winrate_dict[df_matches.iloc[i][f'radiant_hero_{r}']] = \
                    {'matches': 1, 'wins': int(df_matches.iloc[i]['radiant_win'])}
            if hero_winrate_dict.get(df_matches.iloc[i][f'dire_hero_{r}']):
                hero_winrate_dict[df_matches.iloc[i][f'dire_hero_{r}']]['matches'] += 1
                hero_winrate_dict[df_matches.iloc[i][f'dire_hero_{r}']]['wins'] += \
                    (1 - int(df_matches.iloc[i]['radiant_win']))
            else:
                hero_winrate_dict[df_matches.iloc[i][f'dire_hero_{r}']] = \
                    {'matches': 1, 'wins': 1 - int(df_matches.iloc[i]['radiant_win'])}
    df_herowin = pd.DataFrame.from_dict(hero_winrate_dict, orient='index')
    df_herowin['win_pct'] = df_herowin['wins'] / df_herowin['matches'] * 100
    df_herowin.sort_values(by=['win_pct'], ascending=False, inplace=True)
    df_herowin.to_parquet(save_filepath)
    return None


def update_relative_teammate_winrate(df_row, dict_to_update):
    for r in range(1, 6):
        for d in range(1, 6):
            dict_to_update[df_row[f'radiant_hero_{r}']][df_row[f'radiant_hero_{d}']]['matches'] += 1
            dict_to_update[df_row[f'radiant_hero_{r}']][df_row[f'radiant_hero_{d}']]['wins'] += \
                int(df_row['radiant_win'])

            dict_to_update[df_row[f'dire_hero_{r}']][df_row[f'dire_hero_{d}']]['matches'] += 1
            dict_to_update[df_row[f'dire_hero_{r}']][df_row[f'dire_hero_{d}']]['wins'] += \
                1 - int(df_row['radiant_win'])
    return dict_to_update


def update_relative_opponent_winrate(df_row, dict_to_update):
    for r in range(1, 6):
        for d in range(1, 6):
            dict_to_update[df_row[f'radiant_hero_{r}']][df_row[f'dire_hero_{d}']]['matches'] += 1
            dict_to_update[df_row[f'radiant_hero_{r}']][df_row[f'dire_hero_{d}']]['wins'] += \
                int(df_row['radiant_win'])

            dict_to_update[df_row[f'dire_hero_{r}']][df_row[f'radiant_hero_{d}']]['matches'] += 1
            dict_to_update[df_row[f'dire_hero_{r}']][df_row[f'radiant_hero_{d}']]['wins'] += \
                1 - int(df_row['radiant_win'])
    return dict_to_update

def calculate_win_pct(row_entry):
    return row_entry['wins'] / row_entry['matches'] * 100 if row_entry['matches'] > 0 else 0


def calculate_relative_diff(df):
    for i in range(len(df.index)):
        for j in range(len(df.columns)): # should be the same length
            probability_correction = (df.iloc[i, i] + df.iloc[j, j])/2
            df.iloc[i, j] = df.iloc[i, j] - probability_correction
    return df


def relative_hero_win_rate(save_filepath):
    """The relative change in win rate when playing with a given hero - the hero win rate is the baseline"""
    filepath = 'data_storage/public_match_data_formatted.parquet'
    df_matches = pd.read_parquet(filepath)
    # Dataframe of heroes:
    hero_dictionary = get_hero_dict()
    hero_winrate_dict = {}
    for val1 in hero_dictionary.values():
        hero_winrate_dict[val1] = {}
        for val2 in hero_dictionary.values():
            hero_winrate_dict[val1][val2] = {'matches': 0, 'wins': 0}
    hero_opp_winrate_dict = copy.deepcopy(hero_winrate_dict)
    df_matches.apply(lambda row: update_relative_teammate_winrate(row, hero_winrate_dict), axis=1)
    df_matches.apply(lambda row: update_relative_opponent_winrate(row, hero_opp_winrate_dict), axis=1)

    # Teammate win rates:
    df_hero_teammate = pd.DataFrame.from_dict(hero_winrate_dict, orient='index')
    df_teammate_absolute = df_hero_teammate.applymap(calculate_win_pct)
    df_teammate_absolute.sort_index(ascending=True, inplace=True)
    columns_in_order = sorted(df_teammate_absolute.columns.tolist())
    df_teammate_absolute = df_teammate_absolute[columns_in_order]
    # Calculate relative % win probability by adjusting for hero win rates:
    df_teammate_absolute = calculate_relative_diff(df_teammate_absolute)
    df_teammate_absolute.to_parquet(save_filepath + 'teammate')
    # Opponent win rates:
    df_hero_opponents = pd.DataFrame.from_dict(hero_winrate_dict, orient='index')
    df_opponent_absolute = df_hero_opponents.applymap(calculate_win_pct)
    df_opponent_absolute.sort_index(ascending=True, inplace=True)
    columns_in_order = sorted(df_opponent_absolute.columns.tolist())
    df_opponent_absolute = df_opponent_absolute[columns_in_order]
    # Calculate relative % win probability by adjusting for hero win rates:
    df_opponent_absolute = calculate_relative_diff(df_opponent_absolute)
    df_opponent_absolute.to_parquet(save_filepath + 'opponent')
    return None


if __name__ == '__main__':
    # file_path_to_save = 'data_storage/public_match_data_hero_winrate'
    # hero_winrate(file_path_to_save)
    file_path_to_save = 'data_storage/public_match_data_winrate'
    relative_hero_win_rate(file_path_to_save)