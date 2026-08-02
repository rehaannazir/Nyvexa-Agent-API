# These tests check the /leads/extract endpoint.
# Instead of really calling the Gemini AI model (which costs money and
# needs internet), we temporarily replace the function that calls it
# with our own simple fake function that just returns pretend data.
# We save the real function first, and put it back at the end of the
# test, so it doesn't affect any other test.

import app.services.lead_services as lead_services_module
from app.models.lead import Lead, UrgencyLevel
from tests.helpers import make_test_client, register_and_login


def test_extract_lead_without_logging_in_fails():

    client = make_test_client()

    # No "Authorization" header is sent, so this should be rejected.
    response = client.post("/leads/extract", json={"text": "Hello, I need help."})

    assert response.status_code == 401


def test_extract_lead_returns_lead_information():

    client = make_test_client()
    headers = register_and_login(client)

    # This is the pretend lead we want the "AI" to return.
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

    # Our own fake version of lead_extraction. It looks like the real
    # one (it's "async" and takes the same arguments) but instead of
    # calling the AI, it just returns fake_lead straight away.
    async def fake_lead_extraction(message, session, user, request):
        return fake_lead

    # Remember the real function so we can put it back afterwards.
    real_lead_extraction = lead_services_module.LeadService.lead_extraction

    # Swap the real function for our fake one.
    lead_services_module.LeadService.lead_extraction = fake_lead_extraction

    response = client.post(
        "/leads/extract",
        json={"text": "Hi, I'm John from Acme Corp, please call me."},
        headers=headers,
    )

    # Put the real function back so it doesn't affect other tests.
    lead_services_module.LeadService.lead_extraction = real_lead_extraction

    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["company"] == "Acme Corp"


def test_extract_lead_needs_a_text_field():

    client = make_test_client()
    headers = register_and_login(client)

    # We forgot to include "text" in the request body.
    response = client.post("/leads/extract", json={}, headers=headers)

    assert response.status_code == 422


def test_extract_lead_returns_404_if_the_model_fails():

    client = make_test_client()
    headers = register_and_login(client)

    # This time, pretend the AI could not extract anything useful.
    async def fake_lead_extraction(message, session, user, request):
        return None

    real_lead_extraction = lead_services_module.LeadService.lead_extraction
    lead_services_module.LeadService.lead_extraction = fake_lead_extraction

    response = client.post(
        "/leads/extract",
        json={"text": "..."},
        headers=headers,
    )

    lead_services_module.LeadService.lead_extraction = real_lead_extraction

    assert response.status_code == 404
