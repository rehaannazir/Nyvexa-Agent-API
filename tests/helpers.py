def register_and_login(client, email="alice@example.com", password="Password123"):
    """
    Small helper used by the other test files.

    Creates a new user, logs them in, and returns the headers you need
    to send with a request so the API knows who you are.

    Example:
        headers = register_and_login(client)
        client.post("/leads/extract", json={...}, headers=headers)
    """

    client.post(
        "/auth/register",
        json={"name": "alice", "email": email, "passward": password},
    )

    response = client.post(
        "/auth/login", json={"email": email, "passward": password}
    )

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
