import pytest
import jwt
from flask import json
from datetime import datetime, timedelta
from application.app import (
    app,
)


# Fixtures to set up the test client and mock dependencies
@pytest.fixture
def client():
    return app.test_client()


@pytest.fixture
def mock_authentication_service(mocker):
    return mocker.patch(
        "application.controllers.authentication_controller.AuthenticationService"
    )


# Test registration route
def test_register_success(client, mock_authentication_service):
    mock_authentication_service.check_credentials.return_value = True
    mock_authentication_service.generate_2fa.return_value = "mocked_secret"

    response = client.post(
        "/register",
        json={
            "user_id": 1234,
            "email": "test@example.com",
            "password": "password123",
        },
    )
    print("Response data:", response.data)
    data = json.loads(response.data)

    print(data)

    assert response.status_code == 201
    assert (
        data["message"]
        == "Registration successful, scan the QR code in Google Authenticator"
    )
    assert data["secret"] == "mocked_secret"


def test_register_missing_email_password(client):
    response = client.post("/register", json={"email": "", "password": ""})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["error"] == "Email and password are required"


def test_register_invalid_credentials(client, mock_authentication_service):
    mock_authentication_service.check_credentials.return_value = False

    response = client.post(
        "/register", json={"email": "test@example.com", "password": "password1234"}
    )
    data = json.loads(response.data)

    assert response.status_code == 401
    assert data["error"] == "Invalid email or password"


# Test user_secrets route
def test_get_all_user_secrets_success(client, mock_authentication_service):
    mock_authentication_service.get_all_user_secrets.return_value = [
        "secret1",
        "secret2",
    ]

    response = client.get("/user_secrets")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == ["secret1", "secret2"]


def test_get_all_user_secrets_failure(client, mock_authentication_service):
    mock_authentication_service.get_all_user_secrets.side_effect = Exception(
        "Database error"
    )

    response = client.get("/user_secrets")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == []


# Test verify 2FA route
def test_verify_2fa_success(client, mock_authentication_service):
    mock_authentication_service.verify_2fa.return_value = True
    user_id = 1234
    email = "test@example.com"

    # Simulate the expected JWT token generation
    expected_token = jwt.encode(
        {
            "user_id": user_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=1),
        },
        "your_secret_key",
        algorithm="HS256",
    )

    response = client.post(
        "/verify-2fa", json={"user_id": user_id, "email": email, "code": "123456"}
    )
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data["message"] == "2FA verification successful"
    assert data["token"] == expected_token


def test_verify_2fa_invalid_code(client, mock_authentication_service):
    mock_authentication_service.verify_2fa.return_value = False

    response = client.post(
        "/verify-2fa",
        json={
            "user_id": 1234,
            "email": "test@example.com",
            "code": 123456,
        },
    )
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["error"] == "Invalid 2FA code"


def test_verify_2fa_missing_fields(client):
    response = client.post("/verify-2fa", json={"email": "test@example.com"})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["error"] == "Email and 2FA code are required"


def test_verify_2fa_failure(client, mock_authentication_service):
    mock_authentication_service.verify_2fa.side_effect = Exception("Service failure")

    response = client.post(
        "/verify-2fa",
        json={"user_id": 1234, "email": "test@example.com", "code": 123456},
    )
    data = json.loads(response.data)

    assert response.status_code == 500
    assert data["error"] == "Service failure"
