import os

from src.components.data_transformation import PredictionDataCleaner

from src.utils import load_config

cfg = load_config()

latest_dir = cfg["data_storage"]["latest_dir"]
transformed_dir = cfg["data_storage"]["transformed_dir"]
games_to_predict = 0
games_for_prediction = cfg["transformation_parameters"]["games_for_prediction"]

keep_headers = cfg["transformation_parameters"]["keep_headers"]

transformer = PredictionDataCleaner(
    latest_dir, transformed_dir, games_to_predict, games_for_prediction, keep_headers
)

for csv_path in os.listdir(latest_dir):
    transformer.clean_and_append_to_main(csv_path)
transformer.sort_csv()
