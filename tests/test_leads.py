# These tests check the /leads/extract endpoint.
#
# Instead of really calling the Gemini AI model (which costs money and
# needs internet), we "fake" its answer using monkeypatch. This lets us
# test that our own code (the endpoint, the auth check, the response
# format) works correctly, quickly and for free.

from unittest.mock import AsyncMock

from app.models.lead import Lead, UrgencyLevel
from app.services.lead_services import LeadService
from tests.helpers import register_and_login


def test_extract_lead_without_logging_in_fails(client):

    # No "Authorization" header is sent, so this should be rejected.
    response = client.post("/leads/extract", json={"text": "Hello, I need help."})

    assert response.status_code == 401


def test_extract_lead_returns_lead_information(client, monkeypatch):

    headers = register_and_login(client)

    # Pretend the AI already extracted this lead from the text.
    fake_lead = Lead(
        no=1,
        user_id=1,
        name="John Doe",
        company="Acme Corp",
        email="john@example.com",
        headcount=50,
        intent="Wants to buy the product",
        follow_up="1 day",
        urgency=UrgencyLevel.normal,
    )
    monkeypatch.setattr(LeadService, "lead_extraction", AsyncMock(return_value=fake_lead))

    response = client.post(
        "/leads/extract",
        json={"text": "Hi, I'm John from Acme Corp, please call me."},
        headers=headers,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["company"] == "Acme Corp"


def test_extract_lead_needs_a_text_field(client):

    headers = register_and_login(client)

    # We forgot to include "text" in the request body.
    response = client.post("/leads/extract", json={}, headers=headers)

    assert response.status_code == 422


def test_extract_lead_returns_404_if_the_model_fails(client, monkeypatch):

    headers = register_and_login(client)

    # Pretend the AI could not extract anything useful.
    monkeypatch.setattr(LeadService, "lead_extraction", AsyncMock(return_value=None))

    response = client.post(
        "/leads/extract",
        json={"text": "..."},
        headers=headers,
    )

    assert response.status_code == 404
