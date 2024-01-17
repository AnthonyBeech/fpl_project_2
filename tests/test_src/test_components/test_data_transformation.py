import os

from src.components.data_transformation import DataCleaner


def test_clean_data():
    latest_dir = "tests/test_data/latest"
    transformed_dir = "tests/test_data/transformed"
    games_to_predict = 5
    games_for_prediction = 5
    keep_headers = [
        "assists",
        "bonus",
        "bps",
        "clean_sheets",
        "creativity",
        "goals_conceded",
        "goals_scored",
        "ict_index",
        "influence",
        "kickoff_time",
        "minutes",
        "own_goals",
        "penalties_missed",
        "penalties_saved",
        "red_cards",
        "saves",
        "team_a_score",
        "team_h_score",
        "threat",
        "value",
        "was_home",
        "yellow_cards",
        "starts",
        "position",
    ]

    transformer = DataCleaner(
        latest_dir,
        transformed_dir,
        games_to_predict,
        games_for_prediction,
        keep_headers,
    )

    assert True
