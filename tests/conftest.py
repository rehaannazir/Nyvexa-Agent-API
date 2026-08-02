import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.core.database import get_session
from app.main import app


@pytest.fixture()
def client():
    """
    This runs before every test function.

    It creates a brand new, empty database that only lives in memory
    (nothing is saved to a real file), and gives the test a `client`
    object that can call our API endpoints just like a real user would,
    using client.get(...) / client.post(...).

    Because the database is recreated for every single test, tests
    never affect each other and you never need to clean up manually.
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

    # Whenever the app asks for a database session, give it our test one
    # instead of the real one.
    app.dependency_overrides[get_session] = get_test_session

    yield TestClient(app)

    # Undo the override once the test is done.
    app.dependency_overrides.clear()
