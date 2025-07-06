import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient
from main import app
from database.session import get_session

@pytest.fixture(scope="session")
def engine_test():
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture()
def session(engine_test):
    with Session(engine_test) as session:
        yield session

@pytest.fixture(scope="module")
def client(session):
    def get_session_override():
        yield session
    app.dependency_overrides[get_session] = get_session_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
