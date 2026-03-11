import os
import pytest
import requests
import time


@pytest.fixture(scope="session")
def container_url():
    """
    Returns the URL of the running container for container tests.
    Read the CONTAINER_URL environment variable or set default to http://localhost:5000.
    """

    url = os.environ.get("CONTAINER_URL", "http://localhost:5000")

    # wait for the container to be ready
    max_retries = 15
    for i in range(max_retries):
        try:
            response = requests.get(f"{url}/api/health", timeout=2)
            if response.status_code == 200:
                break
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            pass
        time.sleep(2)
    else:
        pytest.fail(f"Container not reachable at {url} after {max_retries} retries")

    return url

