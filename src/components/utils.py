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


def _calculate_fpl_score(row):
    score = 0
    # GKP = 0, DEF = 1, MID = 2, FWD = 3

    # Calculate score based on minutes played
    minutes = row["minutes"]
    if minutes <= 60:
        score += 1
    else:
        score += 2

    # Calculate score for goals and assists
    if row["position"] == 0:
        score += (row["goals_scored"] * 6) + (row["assists"] * 3)
        score += row["clean_sheets"] * 4
        score += (row["saves"] // 3) + (row["penalties_saved"] * 5)
        score += (row["penalties_missed"] * (-2)) + (row["own_goals"] * (-2))
        score += -(row["goals_conceded"] // 2)

    if row["position"] == 1:
        score += (row["goals_scored"] * 6) + (row["assists"] * 3)
        score += row["clean_sheets"] * 4
        score += -(row["goals_conceded"] // 2)

    if row["position"] == 2:
        score += (row["goals_scored"] * 5) + (row["assists"] * 3)
        score += row["clean_sheets"]

    if row["position"] == 3:
        score += (row["goals_scored"] * 4) + (row["assists"] * 3)

    # Calculate score for bonus points
    score += row["bonus"]

    # Calculate score for yellow cards and red cards
    score += (row["yellow_cards"] * (-1)) + (row["red_cards"] * (-3))

    # Own goals
    score += row["own_goals"] * (-2)

    return score
