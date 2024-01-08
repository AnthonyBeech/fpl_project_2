import os
from src.components.data_extraction import LegacyDataExtractor, UpdatePlayerData

years = [20, 21]
source_dir = "tests/test_data/legacy/20yy_yy/players"
extract_dir = "tests/test_data/legacy/exdir"
tmp_dir = "tests/test_data/legacy/tmpdir"
file_pattern = "*/gw.csv"

legacy_dir = "tests/test_data/legacy"
legacy_hide_dir = "tests/test_data/hidden"


def test_legacy_data_extractor():
    extractor = LegacyDataExtractor(
        years, source_dir, extract_dir, tmp_dir, file_pattern
    )
    extractor.make_dirs()
    assert os.path.exists(extract_dir) and os.path.exists(tmp_dir)

    extractor.extract_gw_data()
    assert extractor.players == {"fname1_lname1", "fname_lname"}

    extractor.combine_extracted_data()
    extracted_csv1 = "tests/test_data/legacy/exdir/fname_lname.csv"
    extracted_csv2 = "tests/test_data/legacy/exdir/fname1_lname1.csv"
    assert os.path.exists(extracted_csv1) and os.path.exists(extracted_csv2)

    extractor.cleanup()
    assert not os.path.exists(tmp_dir)


def test_update_player_data(mocker):
    base_url = "https://base/url"
    latest_dir = "tests/test_data/latest"

    mock_global_data = {
        "elements": [0],
    }

    mock_info_from_elements = "fname_lname", "3"  # FWD

    mock_player_data = {
        "history": [
            {
                "element": 5,
                "fixture": 2,
                "opponent_team": 16,
                "total_points": 1,
                "was_home": "true",
                "kickoff_time": "2023-08-12T12:00:00Z",
                "team_h_score": 2,
                "team_a_score": 1,
                "round": 1,
                "minutes": 4,
                "goals_scored": 0,
                "assists": 0,
                "clean_sheets": 0,
                "goals_conceded": 0,
                "own_goals": 0,
                "penalties_saved": 0,
                "penalties_missed": 0,
                "yellow_cards": 0,
                "red_cards": 0,
                "saves": 0,
                "bonus": 0,
                "bps": 2,
                "influence": "0.2",
                "creativity": "0.0",
                "threat": "0.0",
                "ict_index": "0.0",
                "starts": 0,
                "expected_goals": "0.00",
                "expected_assists": "0.00",
                "expected_goal_involvements": "0.00",
                "expected_goals_conceded": "0.02",
                "value": 50,
                "transfers_balance": 0,
                "selected": 2743150,
                "transfers_in": 0,
                "transfers_out": 0,
            },
            {
                "element": 5,
                "fixture": 12,
                "opponent_team": 8,
                "total_points": 1,
                "was_home": "false",
                "kickoff_time": "2023-08-21T19:00:00Z",
                "team_h_score": 0,
                "team_a_score": 1,
                "round": 2,
                "minutes": 20,
                "goals_scored": 0,
                "assists": 0,
                "clean_sheets": 0,
                "goals_conceded": 0,
                "own_goals": 0,
                "penalties_saved": 0,
                "penalties_missed": 0,
                "yellow_cards": 0,
                "red_cards": 0,
                "saves": 0,
                "bonus": 0,
                "bps": 5,
                "influence": "13.0",
                "creativity": "0.0",
                "threat": "0.0",
                "ict_index": "1.3",
                "starts": 0,
                "expected_goals": "0.00",
                "expected_assists": "0.00",
                "expected_goal_involvements": "0.00",
                "expected_goals_conceded": "0.73",
                "value": 50,
                "transfers_balance": -223848,
                "selected": 2639445,
                "transfers_in": 61796,
                "transfers_out": 285644,
            },
        ]
    }

    mocker.patch(
        "src.components.data_extraction._get_global_data",
        return_value=mock_global_data,
    )
    mocker.patch(
        "src.components.data_extraction._get_info_from_elements",
        return_value=mock_info_from_elements,
    )
    mocker.patch(
        "src.components.data_extraction._get_player_data",
        return_value=mock_player_data,
    )

    updater = UpdatePlayerData(base_url, extract_dir, latest_dir)

    updater.process_player_data()

    assert updater.nm == "fname_lname" and updater.position == "3"
    assert os.path.exists(latest_dir)
