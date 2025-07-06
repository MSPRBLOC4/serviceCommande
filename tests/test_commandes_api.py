import pytest
from database import session
from sqlmodel import SQLModel
from database.engine import test_engine
from models.commandes_model import Commandes

@pytest.fixture(scope="session", autouse=True)
def create_tables():
    SQLModel.metadata.create_all(test_engine)
    yield

def test_api_create_and_get_commande(client):
    new_commande = {
        "id": 100,
        "client_id": 1,
        "quantite_total": 3,
        "montant_total": 150.0
    }
    response = client.post("/commandes/", json=new_commande)
    assert response.status_code == 201
    assert response.json()["quantite_total"] == 3

    response_get = client.get(f"/commandes/{new_commande['id']}")
    assert response_get.status_code == 200
    assert response_get.json()["montant_total"] == 150.0

def test_api_commande_not_found(client):
    response = client.get("/commandes/9999")
    assert response.status_code == 404

def test_create_commande_duplicate_id(client):
    data = {
        "id": 101,
        "client_id": 1,
        "quantite_total": 2,
        "montant_total": 200.0
    }
    client.post("/commandes/", json=data)
    response = client.post("/commandes/", json=data)
    assert response.status_code == 400
    assert "déjà existante" in response.json()["detail"]

def test_delete_commande(client):
    data = {
        "id": 102,
        "client_id": 1,
        "quantite_total": 2,
        "montant_total": 100.0
    }
    client.post("/commandes/", json=data)
    response = client.delete("/commandes/102")
    assert response.status_code == 200
    assert "supprimée" in response.json()["detail"]

    response_get = client.get("/commandes/102")
    assert response_get.status_code == 404

def test_get_all_commandes(client):
    client.post("/commandes/", json={"id": 200, "client_id": 1, "quantite_total": 1, "montant_total": 50.0})
    client.post("/commandes/", json={"id": 201, "client_id": 2, "quantite_total": 2, "montant_total": 100.0})
    response = client.get("/commandes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2

def test_update_commande(client):
    client.post("/commandes/", json={"id": 300, "client_id": 1, "quantite_total": 1, "montant_total": 50.0})
    updated = {"id": 300, "client_id": 1, "quantite_total": 5, "montant_total": 250.0}
    response = client.put("/commandes/300", json=updated)
    assert response.status_code == 200
    assert response.json()["quantite_total"] == 5

def test_update_commande_not_found(client):
    updated = {"id": 9999, "client_id": 1, "quantite_total": 5, "montant_total": 250.0}
    response = client.put("/commandes/9999", json=updated)
    assert response.status_code == 404

def test_delete_commande_not_found(client):
    response = client.delete("/commandes/9999")
    assert response.status_code == 404

@pytest.mark.parametrize("bad_data", [
    {"id": "bad", "client_id": 1, "quantite_total": 1, "montant_total": 100.0},
    {"id": -1, "client_id": 1, "quantite_total": 1, "montant_total": 100.0},
    {"id": 1, "client_id": 0, "quantite_total": 1, "montant_total": 100.0},
    {"id": 2, "client_id": 1, "quantite_total": 0, "montant_total": 100.0},
    {"id": 3, "client_id": 1, "quantite_total": 1, "montant_total": -5.0}
])
def test_create_commande_invalid_data(client, bad_data):
    response = client.post("/commandes/", json=bad_data)
    assert response.status_code == 422

def test_delete_then_delete_again(client):
    data = {"id": 600, "client_id": 1, "quantite_total": 2, "montant_total": 100.0}
    client.post("/commandes/", json=data)
    response = client.delete("/commandes/600")
    assert response.status_code == 200

    response = client.delete("/commandes/600")
    assert response.status_code == 404

def test_get_commande_invalid_id_type(client):
    response = client.get("/commandes/bad_id")
    assert response.status_code == 422
