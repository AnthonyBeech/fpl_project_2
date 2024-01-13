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

    def _impute(self):
        imputer = SimpleImputer(strategy="median")
        self.df = pd.DataFrame(imputer.fit_transform(self.df), columns=self.df.columns)

    def _overlap_data(self):
        result_df = self.df.copy()
        N = self.overlap

        if N == 0:
            return

        for i in range(1, N + 1):
            # Shift the DataFrame
            shifted_df = self.df.shift(-i)
            shifted_df.columns = [f"{col}_{i}" for col in self.df.columns]
            result_df = pd.concat([result_df, shifted_df], axis=1)

        self.df = result_df.iloc[:-N, :]

    def _append_df_to_csv(self):
        out_csv = self.transformed_dir + "/transformed.csv"

        file_exists = os.path.isfile(out_csv)
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
        self._overlap_data()

        logging.info(f"Appending {csv} to {self.csv_path}")

        self._append_df_to_csv()
