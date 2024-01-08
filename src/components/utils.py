import os
import re
import pandas as pd

from src.logger import logging



def _replace_years(year_string, year):
    return year_string.replace("yy_yy", f"{year}-{year+1}")


def _get_player_name(filepath):
    player_name_with_tag = os.path.basename(
        os.path.dirname(filepath)
    )  # fname_lname_034
    player_name = re.sub(r"_\d+", "", player_name_with_tag)  # fname_lname
    return player_name


def _get_info_from_elements(sdata, ID):
    fnm = sdata["elements"][ID]["first_name"]
    lnm = sdata["elements"][ID]["second_name"]
    nm = f"{fnm}_{lnm}.csv"
    position = sdata["element_types"][sdata["elements"][ID]["element_type"] - 1]["id"]
    return nm, position


def _find_data_not_in_latest(edata, df):
    # reversed so that most recent is at top
    edata_r = list(reversed(edata["history"]))

    most_recent_kickoff = df["kickoff_time"].max()

    for i, data in enumerate(edata_r):
        if data["kickoff_time"] == most_recent_kickoff:
            break
        
    logging.info(f"{i} rows to add")

    return pd.DataFrame(edata_r[:i])
