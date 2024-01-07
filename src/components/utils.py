import os
import re

def _replace_years(year_string, year):
        return year_string.replace("yy_yy", f"{year}-{year+1}")
    
def _get_player_name(filepath):
        player_name_with_tag = os.path.basename(
            os.path.dirname(filepath)
        )  # fname_lname_034
        player_name = re.sub(r"_\d+", "", player_name_with_tag)  # fname_lname
        return player_name