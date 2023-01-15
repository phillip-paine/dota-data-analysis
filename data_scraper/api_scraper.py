import numpy as np
import pandas as pd
import requests
import json


def account_matches(accountid: int, filepath: str):
    req = requests.get(f'https://api.opendota.com/api/players/{accountid}/matches')
    req_json = req.json()  # convert to json format
    write_json(filepath, req_json)
    return None


def account_recent_match(accountid: int, filepath: str):
    req = requests.get(f'https://api.opendota.com/api/players/{accountid}/recentMatches')
    req_json = req.json()  # convert to json format
    write_json(filepath, req_json)
    return None


def account_wordcloud(accountid: int, filepath: str):
    req = requests.get(f'https://api.opendota.com/api/players/{accountid}/worldcloud')
    req_json = req.json()  # convert to json format
    write_json(filepath, req_json)
    return None


def account_wardmap(accountid: int, filepath: str):
    req = requests.get(f'https://api.opendota.com/api/players/{accountid}/wardmap')
    req_json = req.json()  # convert to json format
    write_json(filepath, req_json)
    return None


def match_report(match_id: int, filepath: str):
    req = requests.get(f'https://api.opendota.com/api/matches/{match_id}')
    req_json = req.json()  # convert to json format
    write_json(filepath, req_json)
    return None


def public_matches(filepath: str):
    req = requests.get(f'https://api.opendota.com/api/publicMatches')
    req_json = req.json()  # convert to json format
    write_json(filepath, req_json)
    return None

def write_json(filename: str, json_object: dict):
    full_filename = '.'.join([filename, 'json'])
    with open(full_filename, 'w') as out:
        json.dump(json_object, out, sort_keys=True, indent='\t')
    return None


