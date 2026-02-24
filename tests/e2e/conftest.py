import pytest
import requests
import time

@pytest.fixture(scope="session")
def local_server():
    """Returns the URL of the live Flask server for E2E tests."""
    url = "http://127.0.0.1:5005"
    
    # Wait for the server to be ready
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.get(f"{url}/api/health")
            if response.status_code == 200:
                break
        except requests.exceptions.ConnectionError:
            pass
        time.sleep(1)
    else:
        pytest.fail("E2E server not reachable at " + url)
        
    return url

