# integration tests
from models import Event, RSVP
import datetime
import pytest

# api test
def test_health_check(client):
    """Tests that the health endpoint returns healthy"""
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def register_user(client):
    response = client.post("/api/auth/register", json={
        "username": "test",
        "password": "test"
    })
    return response

def test_auth_register(client):
    """Tests user creation"""
    # arrange & act
    response = register_user(client)
    # assert
    assert response.status_code == 201
    assert response.json["user"]["username"] == "test"


def test_auth_register_only_first_user_is_admin(client):
    """Tests if first user becomes admin and second user not"""
    # arrange: create a user
    response = client.post("/api/auth/register", json={
        "username": "test1",
        "password": "test"
    })
    assert response.status_code == 201
    assert response.json["user"]["username"] == "test1"
    assert response.json["user"]["is_admin"]

    # act: create duplicate user
    response = client.post("/api/auth/register", json={
        "username": "test2",
        "password": "test"
    })
    # assert
    assert response.status_code == 201
    assert response.json["user"]["username"] == "test2"
    assert not response.json["user"]["is_admin"]


def test_auth_register_missing_field(client):
    """Tests failed user creation with missing input field"""
    # arrange & act
    response = client.post("/api/auth/register", json={
        "username": "test"
    })
    # assert
    assert response.status_code == 400

def test_auth_register_duplicate_name(client):
    """Tests failed user creation with duplicate name"""
    # arrange: create a user
    response = register_user(client)

    # act: create duplicate user
    response = register_user(client)
    # assert
    assert response.status_code == 400


def login_user(client):
    response = client.post("/api/auth/login", json={
        "username": "test",
        "password": "test"
    })
    return response

def test_auth_login(client):
    """Tests user login and jwt token creation"""
    # arrange: create a user
    response = register_user(client)

    # act: login user
    response = login_user(client)
    # assert
    assert response.status_code == 200
    assert response.json["user"]["username"] == "test"

    token = response.json["access_token"]
    # a JWT must have 2 dots (3 parts)
    assert len(token.split('.')) == 3

def create_event(client, data):
    '''Creates an event with the given json data'''
    # arrange: create a user
    response = register_user(client)

    # arrange: login user
    response = login_user(client)
    token = response.json["access_token"]

    # act: create event
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post("/api/events",
        json=data,
        headers=headers
    )

    return response, headers

def test_events(client):
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

    response, _ = create_event(client, data)

    assert response.status_code == 201
    for key in data.keys():
        if key == "date":
            assert response.json["date"] == now.replace(tzinfo=None).isoformat()
        else:
            assert response.json[key] == data[key]


def test_events_with_no_token(client):
    """Tests failed unauthorized event creation"""
    # arrange: create a user
    response = register_user(client)

    # arrange: login user
    response = login_user(client)

    # act: create event
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

    response = client.post("/api/events",
        json=data
    )

    assert response.status_code == 401

# test_rsvp_to_public_event_succeeds_without_auth
def test_rsvps_to_public_without_auth(client):
    '''Tests rsvp to public event without auth'''
    # arrange: create event
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

    response, _ = create_event(client, data)

    event_id = response.json["id"]

    # act
    response = client.post(f"/api/rsvps/event/{event_id}", json = {
        "attending": True
    })

    # assert
    assert response.status_code == 201
    assert response.json["event_id"] == event_id


def test_rsvps_to_private_with_auth(client):
    '''Tests rsvp to private event with auth'''
    # arrange: create event
    now = datetime.datetime.now(datetime.timezone.utc)
    data = {
        "title": "test",
        "description": "test",
        "date": now.isoformat(),
        "location": "test",
        "capacity": 50,
        "is_public": False,
        "requires_admin": False
    }

    response, headers = create_event(client, data)

    event_id = response.json["id"]

    # act
    response = client.post(f"/api/rsvps/event/{event_id}",
        json = {
            "attending": True
        },
        headers=headers
    )

    # assert
    assert response.status_code == 201
    assert response.json["event_id"] == event_id


def test_rsvps_to_private_without_auth(client):
    '''Tests rsvp to private event without auth'''
    # arrange: create event
    now = datetime.datetime.now(datetime.timezone.utc)
    data = {
        "title": "test",
        "description": "test",
        "date": now.isoformat(),
        "location": "test",
        "capacity": 50,
        "is_public": False,
        "requires_admin": False
    }

    response, _ = create_event(client, data)

    event_id = response.json["id"]

    # act
    response = client.post(f"/api/rsvps/event/{event_id}",
        json = {
            "attending": True
        }
    )

    # assert
    assert response.status_code == 401


def test_get_all_events(client):
    """Tests that we can get a list of events from the API"""
    response = client.get("/api/events")
    # assuming the list of events is at least returned (even if empty)
    assert response.status_code == 200
    assert isinstance(response.json, list)


# model test
# need the db fixture for the test
# need the app fixture to setup the db
def test_event_to_dict(app, db):
    now = datetime.datetime.now(datetime.timezone.utc)
    # arrange
    event = Event(
        title="test",
        description="test",
        date=now,
        created_by=1,
        capacity=1
    )
    # actually commit event to db
    db.session.add(event)
    db.session.commit()
    rsvp = RSVP(event_id=event.id, user_id=42, attending=True)
    db.session.add(rsvp)
    db.session.commit()
    # act
    data = event.to_dict()
    # assert
    assert data["title"] == "test"
    assert data["description"] == "test"
    assert data["date"] == now.replace(tzinfo=None).isoformat()
    assert data["created_by"] == 1
    assert data["capacity"] == 1
    assert data["rsvp_count"] == 1


## OPTIONAL TODO: use parametrization feature of pytest
#example:
#@pytest.mark.parametrize("payload, expected_status, expected_error", [
#    # missing title
#    ({"date": "2026-05-01T12:00:00Z"}, 400, "Title is required"),
#
#    # missing date
#    ({"title": "test"}, 400, "Date is required"),
#
#    # invalid date format
#    ({"title": "test", "date": "next Tuesday"}, 400, "Invalid date format"),
#
#    # empty payload
#    ({}, 400, "Title is required")
#])
#
#
#def test_create_event_validation(client, payload, expected_status, expected_error, app):
#    # We need a token because the route has @jwt_required()
#    # Assuming you have a helper to get a token
#    token = "your_valid_test_token" 
#    headers = {"Authorization": f"Bearer {token}"}
#
#    now = datetime.datetime.now(datetime.timezone.utc)
#    data = payload
#    response = create_event(client, data)
#
#    response = client.post('/api/events', json=payload, headers=headers)
#
#    assert response.status_code == expected_status
#    assert expected_error in response.json['error']
