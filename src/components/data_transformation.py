import os
import shutil
import pandas as pd

from sklearn.impute import SimpleImputer


from src.logger import logging
from src.components.utils import _calculate_fpl_score


class DataCleaner:
    def __init__(self, latest_dir, transformed_dir, overlap, keep_headers) -> None:
        self.latest_dir = latest_dir
        self.transformed_dir = transformed_dir
        self.overlap = overlap
        self.keep_headers = keep_headers

        self.original_df = None  # Save df before imputing and other trznsforms

        self._create_transformed_dir()

    def _create_transformed_dir(self):
        if os.path.exists(self.transformed_dir):
            shutil.rmtree(self.transformed_dir)
        os.makedirs(self.transformed_dir, exist_ok=True)

    def _load_data(self):
        self.df = pd.read_csv(self.csv_path)
        logging.info(f"{len(self.df)} rows loaded")

    def _keep_headers(self):
        self.df = self.df[self.keep_headers]

    def _convert_time(self):
        # Time before first legacy data
        epoch = pd.Timestamp("2015-01-01", tz="UTC")

        self.df["kickoff_time"] = (
            (pd.to_datetime(self.df["kickoff_time"]) - epoch)
            .astype("timedelta64[s]")
            .astype(int)
        )

    def _calculate_points(self):
        self.df["points"] = self.df.apply(_calculate_fpl_score, axis=1)

    def _format_headers(self):
        object_cols = ["was_home", "position"]
        int_cols = [col for col in self.keep_headers if col not in object_cols]

        self.df[int_cols] = self.df[int_cols].astype(int)
        self.df[object_cols] = self.df[object_cols].astype(object)
        
    def _remove_players_with_low_mins(self):
        average_minutes_per_player = self.df.groupby('player')['minutes'].mean()

        # Filter players with an average of 7 minutes or more
        keep_players = average_minutes_per_player[average_minutes_per_player >= 32].index

        # Filter the original DataFrame to keep only these players
        self.df = self.df[self.df['player'].isin(keep_players)]

    def _impute(self):
        imputer = SimpleImputer(strategy="median")
        self.df = pd.DataFrame(imputer.fit_transform(self.df), columns=self.df.columns)

    def _overlap_data(self):
        if self.overlap == 0:
            self.df = self.df.drop('player', axis=1)
            return 0

        N = self.overlap
        result_df = self.df.copy()
    
        if len(self.df) >= N + 1:
            for i in range(1, N + 1):
                shifted_df = self.df.shift(-i)
                shifted_df.columns = [f"{col}_{i}" for col in self.df.columns]
                result_df = pd.concat([result_df, shifted_df], axis=1)

            result_df = result_df.iloc[:-(N), :]

        # Rename the original columns with _0 suffix
        n_cols = len(self.df.columns)
        new_column_names = [f"{col}_{0}" if i < n_cols else col for i, col in enumerate(result_df.columns)]
        result_df.columns = new_column_names

        # Drop the 'player' columns from the shifted DataFrames
        columns_to_drop = [col for col in result_df.columns if 'player_' in col]
        result_df = result_df.drop(columns=columns_to_drop)

        self.df = result_df
        
    def _select_training_cols(self):
        N = self.overlap
        points_sum = 0
        
        for i in range(N//2+1, N+1):
            points_column = f"points_{i}"
            if points_column in self.df.columns:
                points_sum += self.df[points_column]     
                
        drop_cols = [col for col in self.df.columns if int(col.split("_")[-1]) > N//2]
        
        self.df[f"{N//2}day_points"] = points_sum
        
        logging.info(f"Calculating {N//2}day_points")
        
        self.df = self.df.drop(drop_cols, axis=1)

             
    def _append_df_to_csv(self):
        out_csv = self.transformed_dir + "/transformed.csv"

        file_exists = os.path.isfile(out_csv)
        if f"points_{self.overlap // 2}" in self.df.columns:
            self.df.to_csv(out_csv, mode="a", header=not file_exists, index=False)

        # Also save without imputing for analysis
        base, extension = os.path.splitext(out_csv)
        out_csv_orig = f"{base}_orig{extension}"

        file_exists = os.path.isfile(out_csv_orig)
        self.original_df.to_csv(out_csv_orig, mode="a", header=not file_exists, index=False)

    def clean_and_append_to_main(self, csv):
        logging.info(f"Loading {csv}")

        self.csv_path = os.path.join(self.latest_dir, csv)

        logging.info(f"Cleaning {csv}")

        self._load_data()
        self._convert_time()
        self._calculate_points()

        self._keep_headers()

        self.original_df = self.df  # copy original df before imputing

        logging.info(f"Formatting {csv} for training")

        #  self._impute()  # Not needed as data is complete
        self._format_headers()
        self._remove_players_with_low_mins()
        
        final_keep_cols = [
            "player",
            "kickoff_time",
            "position",
            "minutes",
            "value",
            "bps",
            "ict_index",
            "points"]
        
        self.df = self.df[final_keep_cols]
        
        self._overlap_data()
        
        self._select_training_cols()

        logging.info(f"Appending {csv} to {self.csv_path}")

        self._append_df_to_csv()
