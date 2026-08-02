# These tests check the /assistant/ endpoint.
#
# Just like in test_leads.py, we fake the AI's reply with monkeypatch
# instead of really calling Gemini and running the tool loop.

from unittest.mock import AsyncMock

from app.routers import assistant as assistant_router
from tests.helpers import register_and_login


def test_assistant_without_logging_in_fails(client):

    response = client.post("/assistant/", json={"message": "Hello"})

    assert response.status_code == 401


def test_assistant_returns_a_reply(client, monkeypatch):

    headers = register_and_login(client)

    # Pretend the AI already replied with this text.
    monkeypatch.setattr(
        assistant_router, "get_response", AsyncMock(return_value="Hi there! How can I help?")
    )

    response = client.post("/assistant/", json={"message": "Hello"}, headers=headers)

    assert response.status_code == 200
    assert response.json() == {"response": "Hi there! How can I help?"}


def test_assistant_rejects_an_empty_message(client):

    headers = register_and_login(client)

    response = client.post("/assistant/", json={"message": ""}, headers=headers)

    assert response.status_code == 422


def test_assistant_rejects_a_message_that_is_too_long(client):

    headers = register_and_login(client)

    too_long_message = "a" * 4001

    response = client.post(
        "/assistant/", json={"message": too_long_message}, headers=headers
    )

    assert response.status_code == 422


def test_assistant_returns_404_if_the_model_fails(client, monkeypatch):

    headers = register_and_login(client)

    monkeypatch.setattr(assistant_router, "get_response", AsyncMock(return_value=None))

    response = client.post("/assistant/", json={"message": "Hello"}, headers=headers)

    assert response.status_code == 404
