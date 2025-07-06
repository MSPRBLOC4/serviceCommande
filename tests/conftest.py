import pytest
from sqlmodel import SQLModel, Session, create_engine
from fastapi.testclient import TestClient
from main import app
from database.session import get_session
from models.commandes_model import Commandes  # assure-toi que ce modèle est bien importé
from database.engine import test_engine
from sqlalchemy import text


@pytest.fixture(scope="session", autouse=True)
def create_test_db():

    SQLModel.metadata.create_all(test_engine)
    yield

@pytest.fixture(scope="function")
def session():
    with Session(test_engine) as session:
        yield session
        session.exec(text("DELETE FROM commandes"))
        session.commit()
@pytest.fixture(scope="function")
def client(session):
    def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
