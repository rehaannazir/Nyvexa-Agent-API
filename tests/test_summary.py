# These tests check the /summary/ endpoint.
# Just like in test_leads.py, instead of really calling Gemini, we
# swap out the function that calls it with our own simple fake
# function, and put the real one back afterwards.

import app.services.summary_services as summary_services_module
from app.models.summary import Summary
from tests.helpers import make_test_client, register_and_login


def test_summary_without_logging_in_fails():

    client = make_test_client()

    response = client.post("/summary/", json={"text": "Some text to summarize."})

    assert response.status_code == 401


def test_summary_returns_a_summary():

    client = make_test_client()
    headers = register_and_login(client)

    # This is the pretend summary we want the "AI" to return.
    fake_summary = Summary(
        no=1,
        user_id=1,
        title="Sample Title",
        summary="Sample summary text.",
        keypoints=["Point one", "Point two"],
    )

    # Our own fake version of fetch_summary.
    async def fake_fetch_summary(text, session, user):
        return fake_summary

    real_fetch_summary = summary_services_module.SummaryService.fetch_summary
    summary_services_module.SummaryService.fetch_summary = fake_fetch_summary

    response = client.post(
        "/summary/",
        json={"text": "Some long text to summarize."},
        headers=headers,
    )

    summary_services_module.SummaryService.fetch_summary = real_fetch_summary

    assert response.status_code == 200
    assert response.json()["title"] == "Sample Title"
    assert response.json()["keypoints"] == ["Point one", "Point two"]


def test_summary_needs_a_text_field():

    client = make_test_client()
    headers = register_and_login(client)

    response = client.post("/summary/", json={}, headers=headers)

    assert response.status_code == 422


def test_summary_returns_404_if_the_model_fails():

    client = make_test_client()
    headers = register_and_login(client)

    # This time, pretend the AI could not summarize the text.
    async def fake_fetch_summary(text, session, user):
        return None

    real_fetch_summary = summary_services_module.SummaryService.fetch_summary
    summary_services_module.SummaryService.fetch_summary = fake_fetch_summary

    response = client.post(
        "/summary/",
        json={"text": "Some text."},
        headers=headers,
    )

    summary_services_module.SummaryService.fetch_summary = real_fetch_summary

    assert response.status_code == 404
