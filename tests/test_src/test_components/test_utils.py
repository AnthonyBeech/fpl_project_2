from src.components.utils import _get_player_name, _replace_years

def test_replace_years():
    test_str = "---yy_yy---"
    year = 12
    
    rep = _replace_years(test_str, year)
    
    assert rep == "---12-13---"
    
def test_get_player_name():
    path = "year/players/fname_lname/gw.csv"
    name = _get_player_name(path)
    assert name == "fname_lname"