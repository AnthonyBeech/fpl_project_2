from src.components.data_extraction import UpdatePlayerData

from src.utils import load_config

cfg = load_config()

base_url = cfg["base_url"]
extraced_legacy_dir = cfg["data_storage"]["extraced_legacy_dir"]
latest_dir = cfg["data_storage"]["latest_dir"]
tmp_dir = cfg["data_storage"]["tmp_dir"]


updater = UpdatePlayerData(base_url, extraced_legacy_dir, latest_dir, tmp_dir)

updater.process_player_data()

updater.cleanup()
