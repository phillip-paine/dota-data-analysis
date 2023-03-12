"""Run complete model from scraped data to returning fitted model"""
from data_predictor.feature_run import main_feature_run
from data_formatter.main_data_formatter import main_formatter_run
from data_predictor.model_run import main_model_run


def main():
    main_formatter_run()
    main_feature_run()
    main_model_run()
    return None


if __name__ == '__main__':
    main()