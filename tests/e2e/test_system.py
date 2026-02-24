import requests
import datetime

def test_health_check_e2e(local_server):
    """Tests that the health endpoint returns healthy"""
    response = requests.get(f"{local_server}/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def register_user_e2e(local_server):
    """Helper function to register a user"""
    response = requests.post(f"{local_server}/api/auth/register", json={
        "username": "test",
        "password": "test"
    })
    return response

def test_auth_register_only_first_user_is_admin_e2e(local_server):
    """Tests if first user becomes admin and second user not"""
    # This must be the first registration test to ensure a clean DB state
    response = requests.post(f"{local_server}/api/auth/register", json={
        "username": "test1",
        "password": "test"
    })
    assert response.status_code == 201
    assert response.json()["user"]["username"] == "test1"
    assert response.json()["user"]["is_admin"]

    response = requests.post(f"{local_server}/api/auth/register", json={
        "username": "test2",
        "password": "test"
    })
    assert response.status_code == 201
    assert response.json()["user"]["username"] == "test2"
    assert not response.json()["user"]["is_admin"]

def test_auth_register_e2e(local_server):
    """Tests user creation"""
    response = register_user_e2e(local_server)
    # If test1/test2 already exist, this might fail with 400 if username is already "test"
    # But since it's "test", it's fine.
    assert response.status_code == 201
    assert response.json()["user"]["username"] == "test"

def test_auth_register_missing_field_e2e(local_server):
    """Tests failed user creation with missing input field"""
    response = requests.post(f"{local_server}/api/auth/register", json={
        "username": "test_missing"
    })
    assert response.status_code == 400

def test_auth_register_duplicate_name_e2e(local_server):
    """Tests failed user creation with duplicate name"""
    # Use a unique name for this test to be sure
    username = "duplicate_user"
    requests.post(f"{local_server}/api/auth/register", json={
        "username": username,
        "password": "test"
    })

    response = requests.post(f"{local_server}/api/auth/register", json={
        "username": username,
        "password": "test"
    })
    assert response.status_code == 400

def login_user_e2e(local_server):
    response = requests.post(f"{local_server}/api/auth/login", json={
        "username": "test",
        "password": "test"
    })
    return response

def test_auth_login_e2e(local_server):
    """Tests user login and jwt token creation"""
    # Ensure "test" user exists
    register_user_e2e(local_server)

    response = login_user_e2e(local_server)
    assert response.status_code == 200
    assert response.json()["user"]["username"] == "test"

    token = response.json()["access_token"]
    assert len(token.split('.')) == 3

def create_event_e2e(local_server, data):
    """Creates an event with the given json data"""
    register_user_e2e(local_server)
    response = login_user_e2e(local_server)
    token = response.json()["access_token"]

    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(f"{local_server}/api/events",
        json=data,
        headers=headers
    )

    return response, headers

def test_events_e2e(local_server):
    """Tests event creation which requires authorization"""
    now = datetime.datetime.now(datetime.timezone.utc)
    data = {
        "title": "test",
        "description": "test",
        "date": now.isoformat(),
        "location": "test",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

    response, _ = create_event_e2e(local_server, data)

    assert response.status_code == 201
    for key in data.keys():
        if key == "date":
            assert response.json()["date"] == now.replace(tzinfo=None).isoformat()
        else:
            assert response.json()[key] == data[key]

def test_events_with_no_token_e2e(local_server):
    """Tests failed unauthorized event creation"""
    register_user_e2e(local_server)
    login_user_e2e(local_server)

    now = datetime.datetime.now(datetime.timezone.utc)
    data = {
        "title": "test",
        "description": "test",
        "date": now.isoformat(),
        "location": "test",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

    response = requests.post(f"{local_server}/api/events",
        json=data
    )

    assert response.status_code == 401

def test_rsvps_to_public_without_auth_e2e(local_server):
    """Tests rsvp to public event without auth"""
    now = datetime.datetime.now(datetime.timezone.utc)
    data = {
        "title": "test_public",
        "description": "test",
        "date": now.isoformat(),
        "location": "test",
        "capacity": 50,
        "is_public": True,
        "requires_admin": False
    }

    response, _ = create_event_e2e(local_server, data)
    event_id = response.json()["id"]

    response = requests.post(f"{local_server}/api/rsvps/event/{event_id}", json = {
        "attending": True
    })

    assert response.status_code == 201
    assert response.json()["event_id"] == event_id

def test_rsvps_to_private_with_auth_e2e(local_server):
    """Tests rsvp to private event with auth"""
    now = datetime.datetime.now(datetime.timezone.utc)
    data = {
        "title": "test_private",
        "description": "test",
        "date": now.isoformat(),
        "location": "test",
        "capacity": 50,
        "is_public": False,
        "requires_admin": False
    }

    response, headers = create_event_e2e(local_server, data)
    event_id = response.json()["id"]

    response = requests.post(f"{local_server}/api/rsvps/event/{event_id}",
        json = {
            "attending": True
        },
        headers=headers
    )

    assert response.status_code == 201
    assert response.json()["event_id"] == event_id

def test_rsvps_to_private_without_auth_e2e(local_server):
    """Tests rsvp to private event without auth"""
    now = datetime.datetime.now(datetime.timezone.utc)
    data = {
        "title": "test_private_noauth",
        "description": "test",
        "date": now.isoformat(),
        "location": "test",
        "capacity": 50,
        "is_public": False,
        "requires_admin": False
    }

    response, _ = create_event_e2e(local_server, data)
    event_id = response.json()["id"]

    response = requests.post(f"{local_server}/api/rsvps/event/{event_id}",
        json = {
            "attending": True
        }
    )

    assert response.status_code == 401

def test_get_all_events_e2e(local_server):
    """Tests getting a list of events"""
    response = requests.get(f"{local_server}/api/events")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
