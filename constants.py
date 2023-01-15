# add hero dictionary from api grab:
import requests
import pickle


def create_update_hero_dict():
    r = requests.get("https://api.opendota.com/api/heroes")
    hero_dict = {}
    hero_json = r.json()
    for line in hero_json:
        hero_dict[line['id']] = line['localized_name']
    f = open('data_scraper/data/hero_dict.pkl', 'wb')
    pickle.dump(hero_dict, f)
    f.close()


if __name__ == '__main__':
    create_update_hero_dict()
