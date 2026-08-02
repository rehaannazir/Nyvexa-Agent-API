from tests.helpers import make_test_client


def test_can_register_a_new_user():

    client = make_test_client()

    response = client.post(
        "/auth/register",
        json={"name": "alice", "email": "alice@example.com", "passward": "Password123"},
    )

    assert response.status_code == 201


def test_cannot_register_with_an_email_already_used():

    client = make_test_client()

    client.post(
        "/auth/register",
        json={"name": "alice", "email": "alice@example.com", "passward": "Password123"},
    )

    response = client.post(
        "/auth/register",
        json={
            "name": "someone_else",
            "email": "alice@example.com",
            "passward": "Password123",
        },
    )

    assert response.status_code == 400


def test_password_must_be_at_least_8_characters():

    client = make_test_client()

    response = client.post(
        "/auth/register",
        json={"name": "bob", "email": "bob@example.com", "passward": "short"},
    )

    assert response.status_code == 400


def test_can_login_with_the_correct_password():

    client = make_test_client()

    client.post(
        "/auth/register",
        json={"name": "alice", "email": "alice@example.com", "passward": "Password123"},
    )

    response = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "passward": "Password123"},
    )

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_cannot_login_with_the_wrong_password():

    client = make_test_client()

    client.post(
        "/auth/register",
        json={"name": "alice", "email": "alice@example.com", "passward": "Password123"},
    )

    response = client.post(
        "/auth/login",
        json={"email": "alice@example.com", "passward": "WrongPassword"},
    )

    assert response.status_code == 404


def test_cannot_login_with_an_email_that_does_not_exist():

    client = make_test_client()

    response = client.post(
        "/auth/login",
        json={"email": "nobody@example.com", "passward": "Password123"},
    )

    assert response.status_code == 404


def test_can_update_username():

    client = make_test_client()

    client.post(
        "/auth/register",
        json={"name": "alice", "email": "alice@example.com", "passward": "Password123"},
    )

    response = client.post(
        "/auth/update-username",
        json={"old_username": "alice", "new_username": "alice_new"},
    )

    assert response.status_code == 200


def test_can_update_email():

    client = make_test_client()

    client.post(
        "/auth/register",
        json={"name": "alice", "email": "alice@example.com", "passward": "Password123"},
    )

    response = client.post(
        "/auth/update-email",
        json={"old_email": "alice@example.com", "new_email": "alice_new@example.com"},
    )

    assert response.status_code == 200
