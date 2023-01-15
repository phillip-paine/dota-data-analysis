import pandas as pd
import datetime

from api_scraper import public_matches


def run_main(publicmatches: bool):
    """run scraper functions"""
    if publicmatches:
        filename = 'data/public_match_data'
        time_suffix = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        public_matches('_'.join([filename, time_suffix]))

    return None


if __name__ == '__main__':
    # scrape public match data from api and write to json:
    for i in range(50):
        run_main(publicmatches=True)