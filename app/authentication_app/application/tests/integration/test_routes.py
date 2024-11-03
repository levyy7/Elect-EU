import pytest
from flask import json
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


def test_register_missing_email_password(client):
    response = client.post("/register", json={"email": "", "password": ""})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["error"] == "Email and password are required"


def test_get_all_user_secrets_failure(client, mock_authentication_service):
    mock_authentication_service.get_all_user_secrets.side_effect = Exception(
        "Database error"
    )

    response = client.get("/user_secrets")
    data = json.loads(response.data)

    assert response.status_code == 200
    assert data == []


def test_verify_2fa_missing_fields(client):
    response = client.post("/verify-2fa", json={"email": "test@example.com"})
    data = json.loads(response.data)

    assert response.status_code == 400
    assert data["error"] == "Email and 2FA code are required"
