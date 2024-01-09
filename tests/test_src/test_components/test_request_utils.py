import requests_mock

from src.components.request_utils import _get_global_data, _get_player_data

base_url = "https://test/site/"
player_id = 0

def test_get_global_data():
    with requests_mock.Mocker() as m:
        m.get(base_url + "bootstrap-static/", json={"key": "value"})
        response = _get_global_data(base_url)

        assert response == {"key": "value"}

    with requests_mock.Mocker() as m:
        m.get(base_url + "bootstrap-static/", status_code=404)
        response = _get_global_data(base_url)

        assert response == None
        

def test_get_player_data():
    with requests_mock.Mocker() as m:
        m.get(base_url + f"element-summary/{player_id}/", json={"key": "value"})
        response = _get_player_data(base_url, player_id)

        assert response == {"key": "value"}

    with requests_mock.Mocker() as m:
        m.get(base_url + f"element-summary/{player_id}/", status_code=404)
        response = _get_player_data(base_url, player_id)

        assert response == None