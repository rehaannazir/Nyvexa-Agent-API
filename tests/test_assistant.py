# These tests check the /assistant/ endpoint.
#
# Just like in test_leads.py, instead of really calling Gemini and
# running the tool loop, we swap out the function that does that with

from app.routers import assistant as assistant_router
from tests.helpers import make_test_client, register_and_login


def test_assistant_without_logging_in_fails():

    client = make_test_client()

    response = client.post("/assistant/", json={"message": "Hello"})

    assert response.status_code == 401


def test_assistant_returns_a_reply():

    client = make_test_client()
    headers = register_and_login(client)

    # Our own fake version of get_response, pretending the AI already
    # replied with this text.
    async def fake_get_response(text, session_id):
        return "Hi there! How can I help?"

    real_get_response = assistant_router.get_response
    assistant_router.get_response = fake_get_response

    response = client.post("/assistant/", json={"message": "Hello"}, headers=headers)

    assistant_router.get_response = real_get_response

    assert response.status_code == 200
    assert response.json() == {"response": "Hi there! How can I help?"}


def test_assistant_rejects_an_empty_message():

    client = make_test_client()
    headers = register_and_login(client)

    response = client.post("/assistant/", json={"message": ""}, headers=headers)

    assert response.status_code == 422


def test_assistant_rejects_a_message_that_is_too_long():

    client = make_test_client()
    headers = register_and_login(client)

    too_long_message = "a" * 4001

    response = client.post(
        "/assistant/", json={"message": too_long_message}, headers=headers
    )

    assert response.status_code == 422


def test_assistant_returns_404_if_the_model_fails():

    client = make_test_client()
    headers = register_and_login(client)

    async def fake_get_response(text, session_id):
        return None

    real_get_response = assistant_router.get_response
    assistant_router.get_response = fake_get_response

    response = client.post("/assistant/", json={"message": "Hello"}, headers=headers)

    assistant_router.get_response = real_get_response

    assert response.status_code == 404
