import requests
import json
import time


def _get_global_data(base_url) -> dict:
    response = requests.get(base_url + "bootstrap-static/")

    if response.status_code != 200:
        return None
    return json.loads(response.text)


def _get_player_data(base_url, player_id: int) -> dict:
    full_url = base_url + f"element-summary/{player_id}/"
    response = ""
    while response == "":
        try:
            response = requests.get(full_url)
        except:
            time.sleep(5)
    if response.status_code != 200:
        return None
    return json.loads(response.text)
