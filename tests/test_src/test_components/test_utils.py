from src.components.utils import (
    _get_player_name,
    _replace_years,
    _calculate_fpl_score,
    _get_info_from_elements,
)


def test_replace_years():
    test_str = "---yy_yy---"
    year = 12

    rep = _replace_years(test_str, year)

    assert rep == "---12-13---"


def test_get_player_name():
    path = "year/players/fname_lname/gw.csv"
    name = _get_player_name(path)
    assert name == "fname_lname"


def test_get_info_from_elements():
    test_data = {
        "elements": [
            {"-": None},
            {"first_name": "fname", "second_name": "lname", "element_type": 1},
        ],
        "element_types": [{"id": 3}],
    }
    ID = 1

    nm, pos = _get_info_from_elements(test_data, ID)

    assert nm == "fname_lname.csv" and pos == 3


def test_calculate_fpl_score():
    test_row = {
        "minutes": 90,
        "position": 0,  # Testing for a Goalkeeper
        "goals_scored": 1,
        "assists": 1,
        "clean_sheets": 1,
        "saves": 3,
        "penalties_saved": 0,
        "penalties_missed": 0,
        "own_goals": 0,
        "goals_conceded": 1,
        "yellow_cards": 1,
        "red_cards": 0,
        "bonus": 3,
    }

    score = _calculate_fpl_score(test_row)

    assert score == 18
