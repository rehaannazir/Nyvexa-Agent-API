# These tests check the /summary/ endpoint.
#
# Just like in test_leads.py, we fake the AI's answer with monkeypatch
# instead of really calling Gemini.

from unittest.mock import AsyncMock

from app.models.summary import Summary
from app.services.summary_services import SummaryService
from tests.helpers import register_and_login


def test_summary_without_logging_in_fails(client):

    response = client.post("/summary/", json={"text": "Some text to summarize."})

    assert response.status_code == 401


def test_summary_returns_a_summary(client, monkeypatch):

    headers = register_and_login(client)

    # Pretend the AI already summarized the text.
    fake_summary = Summary(
        no=1,
        user_id=1,
        title="Sample Title",
        summary="Sample summary text.",
        keypoints=["Point one", "Point two"],
    )
    monkeypatch.setattr(SummaryService, "fetch_summary", AsyncMock(return_value=fake_summary))

    response = client.post(
        "/summary/",
        json={"text": "Some long text to summarize."},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Sample Title"
    assert response.json()["keypoints"] == ["Point one", "Point two"]


def test_summary_needs_a_text_field(client):

    headers = register_and_login(client)

    response = client.post("/summary/", json={}, headers=headers)

    assert response.status_code == 422


def test_summary_returns_404_if_the_model_fails(client, monkeypatch):

    headers = register_and_login(client)

    monkeypatch.setattr(SummaryService, "fetch_summary", AsyncMock(return_value=None))

    response = client.post(
        "/summary/",
        json={"text": "Some text."},
        headers=headers,
    )

    assert response.status_code == 404
