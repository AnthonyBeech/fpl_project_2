import os
import shutil
import glob
from collections import defaultdict
import pandas as pd

from src.logger import logging
from src.components.utils import (
    _replace_years,
    _get_player_name,
    _get_info_from_elements,
    _find_data_not_in_latest,
)
from src.components.request_utils import _get_player_data, _get_global_data


class LegacyDataExtractor:
    def __init__(self, years, source_dir, extract_dir, tmp_dir, file_pattern) -> None:
        self.years = years
        self.source_dir = source_dir
        self.extract_dir = extract_dir
        self.tmp_dir = tmp_dir
        self.file_pattern = file_pattern

    def make_dirs(self):
        os.makedirs(self.extract_dir, exist_ok=True)
        os.makedirs(self.tmp_dir, exist_ok=True)

    def _move_csv(self, filepath, year):
        player_name = _get_player_name(filepath)
        if player_name not in self.players:
            self.players.add(player_name)
            new_filename = f"{player_name}_20{year}.csv"

            new_path = os.path.join(self.tmp_dir, new_filename)

            shutil.copy(filepath, new_path)
        else:
            # player has dupliacte name, can be removed
            pass

    def extract_gw_data(self):
        """Extract the gameweek data from the legacy data"""
        for year in self.years:
            logging.info(f"Extracting year {year}")

            self.players = set()

            # update source dir for each year of data
            source_dir = _replace_years(self.source_dir, year)
            search_str = os.path.join(source_dir, self.file_pattern)
            for filepath in glob.glob(search_str):
                self._move_csv(filepath, year)

    def _combine_files(self, files: list) -> pd.DataFrame:
        sorted_files = sorted(files, key=lambda x: x[0])
        df_list = [pd.read_csv(file[1]) for file in sorted_files]
        return pd.concat(df_list, ignore_index=True)

    def _parse_file_name(self, file_path: str) -> tuple:
        parts = os.path.basename(file_path).split("_")
        base_name = "_".join(parts[:-1])
        year = parts[-1].split(".")[0]
        return base_name, year

    def combine_extracted_data(self):
        player_groups = defaultdict(list)
        search_dir = os.path.join(self.tmp_dir, "*.csv")
        logging.info(f"Combing player gw data from {search_dir}")

        for file_path in glob.glob(search_dir):
            player_name, year = self._parse_file_name(file_path)
            player_groups[player_name].append((year, file_path))

        logging.info(f"{len( player_groups.items())} total players across all data")

        for name, files in player_groups.items():
            combined_df = self._combine_files(files)
            combined_df.to_csv(
                os.path.join(self.extract_dir, f"{name}.csv"), index=False
            )

    def cleanup(self):
        shutil.rmtree(self.tmp_dir)

        logging.info(f"Cleanup complete, {self.tmp_dir} deleted.")


class UpdatePlayerData:
    def __init__(self, base_url, extraced_legacy_dir, latest_dir, tmp_dir) -> None:
        self.base_url = base_url
        self.extraced_legacy_dir = extraced_legacy_dir
        self.latest_dir = latest_dir
        self.tmp_dir = tmp_dir

        self._move_data_and_make_latest_if_first_run()

    def _move_data_and_make_latest_if_first_run(self):
        if not os.path.exists(self.latest_dir):
            os.mkdir(self.latest_dir)
            if os.path.exists(self.tmp_dir):
                shutil.rmtree(self.tmp_dir)
            shutil.copytree(self.extraced_legacy_dir, self.tmp_dir)
        else:
            if os.path.exists(self.tmp_dir):
                shutil.rmtree(self.tmp_dir)
            shutil.copytree(self.latest_dir, self.tmp_dir)
            shutil.rmtree(self.latest_dir)
            os.mkdir(self.latest_dir)

    def _concat_and_save_df(self, dfr, df, id):
        result_df = pd.concat([df, dfr], ignore_index=True)
        result_df["position"] = self.position
        result_df["player"] = id

        result_df.to_csv(f"{self.latest_dir}/{self.nm}")

    def process_player_data(self):
        logging.info(f"Getting player data for processing")

        sdata = _get_global_data(self.base_url)

        nplayers = len(sdata["elements"])

        for player in range(1, nplayers):
            self.nm, self.position, self.id = _get_info_from_elements(sdata, player)

            logging.info(f"Updating player {player}/{nplayers-1}: {self.nm}")

            try:
                df = pd.read_csv(f"{self.tmp_dir}/{self.nm}")
                if "position" in df.columns:
                    df = df.drop(["position"], axis=1)
            except Exception as e:
                logging.warning(f"No player csv at: {self.tmp_dir}/{self.nm}")
                df = pd.DataFrame()

            edata = _get_player_data(self.base_url, self.id)

            if edata is None:
                logging.warning(f"No player {self.id} in API")
                continue

            self.dfr = _find_data_not_in_latest(edata, df)
            if len(df) + len(self.dfr) < 1:
                logging.warning(f"No data for {self.nm} yet")
                continue

            self._concat_and_save_df(self.dfr, df, self.id)

    def cleanup(self):
        """Remove any files not in the current API"""
        if os.path.exists(self.tmp_dir):
            shutil.rmtree(self.tmp_dir)
