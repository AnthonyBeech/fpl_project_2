import os

from src.components.data_transformation import DataCleaner

from src.utils import load_config

cfg = load_config()

latest_dir = cfg["data_storage"]["latest_dir"]
transformed_dir = cfg["data_storage"]["transformed_dir"]
overlap = cfg["transformation_parameters"]["overlap"]
keep_headers = cfg["transformation_parameters"]["keep_headers"] 

transformer = DataCleaner(latest_dir, transformed_dir, overlap, keep_headers)

for csv_path in os.listdir(latest_dir):
    transformer.clean_and_append_to_main(csv_path)
