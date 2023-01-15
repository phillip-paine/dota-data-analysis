import pandas as pd
from data_formatter.utils import get_hero_dict

def hero_winrate(save_filepath):
    filepath = 'data_storage/public_match_data_formatted.csv'
    df_matches = pd.read_csv(filepath)
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
    df_herowin.to_csv(save_filepath)
    return None


def update_relative_winrate_dictionary(df_row, dict_to_update):
    for r in range(1, 6):
        for d in range(1, 6):
            dict_to_update[df_row[f'radiant_hero_{r}']][df_row[f'dire_hero_{d}']]['matches'] += 1
            dict_to_update[df_row[f'radiant_hero_{r}']][df_row[f'radiant_hero_{d}']]['matches'] += 1
            dict_to_update[df_row[f'radiant_hero_{r}']][df_row[f'dire_hero_{d}']]['wins'] += \
                int(df_row['radiant_win'])
            dict_to_update[df_row[f'radiant_hero_{r}']][df_row[f'radiant_hero_{d}']]['wins'] += \
                int(df_row['radiant_win'])

            dict_to_update[df_row[f'dire_hero_{r}']][df_row[f'dire_hero_{d}']]['matches'] += 1
            dict_to_update[df_row[f'dire_hero_{r}']][df_row[f'radiant_hero_{d}']]['matches'] += 1
            dict_to_update[df_row[f'dire_hero_{r}']][df_row[f'dire_hero_{d}']]['wins'] += \
                1 - int(df_row['radiant_win'])
            dict_to_update[df_row[f'dire_hero_{r}']][df_row[f'radiant_hero_{d}']]['wins'] += \
                1 - int(df_row['radiant_win'])
    return dict_to_update


def calculate_win_pct(row_entry):
    return row_entry['wins'] / row_entry['matches'] if row_entry['matches'] > 0 else 0


def calculate_relative_win(row_entry, win_dict):



def relative_hero_win_rate(save_filepath):
    """The relative change in win rate when playing with a given hero - the hero win rate is the baseline"""
    filepath = 'data_storage/public_match_data_formatted.csv'
    df_matches = pd.read_csv(filepath)
    # Dataframe of heroes:
    hero_dictionary = get_hero_dict()
    hero_winrate_dict = {}
    for val1 in hero_dictionary.values():
        hero_winrate_dict[val1] = {}
        for val2 in hero_dictionary.values():
            hero_winrate_dict[val1][val2] = {'matches': 0, 'wins': 0}

    df_matches.apply(lambda row: update_relative_winrate_dictionary(row, hero_winrate_dict), axis=1)

    df_herowin = pd.DataFrame.from_dict(hero_winrate_dict, orient='index')
    df_herowin_absolute = df_herowin.applymap(calculate_win_pct)
    df_herowin_absolute.sort_index(ascending=True, inplace=True)
    df_herowin_absolute = df_herowin_absolute[df_herowin_absolute.columns.tolist()]
    # Calculate relative % win probability by adjusting for hero win rates:
    df_herowin_relative = df_herowin_absolute.applymap()

    df_herowin_relative.to_csv(save_filepath)
    return None


if __name__ == '__main__':
    # file_path_to_save = 'data_storage/public_match_data_hero_winrate'
    # hero_winrate(file_path_to_save)
    file_path_to_save = 'data_storage/public_match_data_hero_relative_winrate'
    relative_hero_win_rate(file_path_to_save)