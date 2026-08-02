# These tests check the /assistant/ endpoint.
#
# The real endpoint streams its reply back piece by piece (Server-Sent
# Events) instead of sending one JSON response at the end. So instead
# of faking get_response as a function that returns a string, we fake
# it as an async generator that yields the same small event dicts the
# real one would.

from app.routers import assistant as assistant_router
from tests.helpers import make_test_client, register_and_login


def test_assistant_without_logging_in_fails():

    client = make_test_client()

    response = client.post("/assistant/", json={"message": "Hello"})

    assert response.status_code == 401


def test_assistant_streams_the_reply():

    client = make_test_client()
    headers = register_and_login(client)

    # Our own fake version of get_response. Just like the real one,
    # it's an "async generator" - instead of returning one value, it
    # yields several small pieces one at a time.
    async def fake_get_response(text, session_id, request):
        yield {"type": "token", "content": "Hi there!"}
        yield {"type": "token", "content": " How can I help?"}

    real_get_response = assistant_router.get_response
    assistant_router.get_response = fake_get_response

    response = client.post("/assistant/", json={"message": "Hello"}, headers=headers)

    assistant_router.get_response = real_get_response

    assert response.status_code == 200
    # The streamed pieces should both show up somewhere in the response.
    assert "Hi there!" in response.text
    assert "How can I help?" in response.text


def test_assistant_streams_tool_call_events():

    client = make_test_client()
    headers = register_and_login(client)

    # Pretend the AI used the calculator tool before answering.
    async def fake_get_response(text, session_id, request):
        yield {"type": "tool_call", "tool": "calculator"}
        yield {"type": "token", "content": "96"}

    real_get_response = assistant_router.get_response
    assistant_router.get_response = fake_get_response

    response = client.post(
        "/assistant/", json={"message": "What is 12 times 8?"}, headers=headers
    )

    assistant_router.get_response = real_get_response

    assert response.status_code == 200
    assert "tool_call" in response.text
    assert "calculator" in response.text


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
