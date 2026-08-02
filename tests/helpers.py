from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.database import get_session
from app.core.limiter import limiter
from app.main import app


def make_test_client():
    """
    Creates a brand new, empty, in-memory database (it disappears when
    the test ends) and returns a TestClient connected to it.

    Call this at the very start of every test, so each test gets its
    own clean database and tests never affect each other.
    """

    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)

    def get_test_session():
        with Session(test_engine) as session:
            yield session

    # Tell the app: "whenever you need a database session, use this
    # test one instead of the real one."
    app.dependency_overrides[get_session] = get_test_session

    # Every request made through TestClient looks like it comes from the
    # same fake IP ("testclient"), so without this, the rate limiter
    # would treat the whole test suite as one client and later tests
    # would start failing with 429 Too Many Requests once earlier tests
    # used up the quota. Resetting it here gives each test a clean slate,
    # just like the fresh database above.
    limiter.reset()

    return TestClient(app)


def register_and_login(client, email="alice@example.com", password="Password123"):
    """
    Creates a user and logs them in.

    Returns the headers you need to send with a request so the API
    knows who you are, e.g.:

        headers = register_and_login(client)
        client.post("/leads/extract", json={...}, headers=headers)
    """

    client.post(
        "/auth/register",
        json={"name": "alice", "email": email, "passward": password},
    )

    response = client.post("/auth/login", json={"email": email, "passward": password})

    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}
