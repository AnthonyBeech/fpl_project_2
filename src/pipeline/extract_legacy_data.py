from src.components.data_extraction import LegacyDataExtractor

from src.utils import load_config

cfg = load_config()

years = cfg["legacy_data"]["years"]
source_dir = cfg["legacy_data"]["source_dir"]

tmp_dir = cfg["data_storage"]["tmp_dir"]
extraced_legacy_dir = cfg["data_storage"]["extraced_legacy_dir"]


extractor = LegacyDataExtractor(years, source_dir, extraced_legacy_dir, tmp_dir)

extractor.extract_gw_data()
extractor.combine_extracted_data()
extractor.cleanup(remove_all_other_legacy=False)
