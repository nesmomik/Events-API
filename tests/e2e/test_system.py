import requests

def test_get_all_events_e2e(e2e_server):
    """
    Tests that we can get a list of events from the API 
    using a real HTTP request against the live server.
    """
    url = f"{e2e_server}/api/events"
    response = requests.get(url)
    
    assert response.status_code == 200
    assert isinstance(response.json(), list)