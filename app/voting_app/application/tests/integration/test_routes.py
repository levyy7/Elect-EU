import pytest
import jwt
import datetime
from application.app import (
    app,
)
from ...exceptions.user_already_exists_error import UserAlreadyExistsError

# from ...exceptions.missing_fields_error import MissingFieldsError


# Fixtures to set up the test client and mock dependencies
@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def mock_vote_service(mocker):
    return mocker.patch("application.controllers.citizen_controller.VoteService")


@pytest.fixture
def mock_user_service(mocker):
    return mocker.patch("application.controllers.citizen_controller.UserService")


@pytest.fixture
def mock_election_service(mocker):
    return mocker.patch("application.controllers.citizen_controller.ElectionService")


@pytest.fixture
def valid_token():
    payload = {
        "user_id": "test_user_id",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
    }
    return jwt.encode(payload, "your_secret_key", algorithm="HS256")


def test_get_election(client, mock_election_service):
    election = {
        "election_id": 1,
        "date": "06-10-2024",
        "vote_options": [
            {
                "vote_option_id": 1,
                "party_name": "party1",
                "candidates": ["name0", "name1", "name2"],
                "photo": "photo1",
            },
            {
                "vote_option_id": 2,
                "party_name": "party2",
                "candidates": ["name0", "name1", "name2"],
                "photo": "photo2",
            },
            {
                "vote_option_id": 3,
                "party_name": "party3",
                "candidates": ["name0", "name1", "name2"],
                "photo": "photo3",
            },
        ],
    }
    mock_election_service.return_value.get_current_election.return_value = election

    response = client.get("/election")
    assert response.status_code == 200
    assert response.json == election


def test_register_citizen_success(client, mock_user_service):
    mock_user_service.return_value.create_user.return_value = None  # Simulate success

    response = client.post(
        "/register",
        json={
            "user_id": "test_user1",
            "email": "test_user1@gmail.com",
            "password": "test_pass",
        },
    )
    assert response.status_code == 200
    assert response.json == {"message": "Citizen created succesfully"}


def test_register_citizen_missing_fields(client):
    response = client.post(
        "/register", json={"user_id": "test_user"}
    )  # Missing password
    assert response.status_code == 400
    assert "error" in response.json


def test_register_citizen_user_already_exists(client, mock_user_service):
    mock_user_service.return_value.create_user.side_effect = UserAlreadyExistsError(
        "User already exists"
    )

    response = client.post(
        "/register",
        json={
            "user_id": "existing_user",
            "email": "existing_user@gmail.com",
            "password": "test_pass",
        },
    )
    assert response.status_code == 402
    assert response.json["error"] == "User already exists"


def test_vote_success(client, mock_vote_service, valid_token):
    mock_vote_service.return_value.vote_in_election.return_value = None

    response = client.post(
        "/vote",
        headers={"Authorization": f"Bearer {valid_token}"},
        json={"user_id": "existing_user", "vote_option_id": "option1"},
    )
    assert response.status_code == 200
    assert response.json == {"message": "Vote submitted successfully."}


def test_vote_missing_auth_header(client):
    response = client.post("/vote", json={"vote_option_id": "option1"})
    assert response.status_code == 401
    assert response.json["error"] == "Authorization token is missing or invalid"


def test_vote_invalid_token(client):
    response = client.post(
        "/vote",
        headers={"Authorization": "Bearer invalid_token"},
        json={"vote_option_id": "option1"},
    )
    assert response.status_code == 401
    assert response.json["error"] == "Invalid token"


def test_vote_expired_token(client):
    expired_token = jwt.encode(
        {
            "user_id": "test_user_id",
            "exp": datetime.datetime.utcnow() - datetime.timedelta(seconds=1),
        },
        "your_secret_key",
        algorithm="HS256",
    )

    response = client.post(
        "/vote",
        headers={"Authorization": f"Bearer {expired_token}"},
        json={"vote_option_id": "option1"},
    )
    assert response.status_code == 401
    assert response.json["error"] == "Token has expired"


def test_vote_missing_fields(client, valid_token):
    response = client.post(
        "/vote", headers={"Authorization": f"Bearer {valid_token}"}, json={}
    )
    assert response.status_code == 400
    assert "error" in response.json
