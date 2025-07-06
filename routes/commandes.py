import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Field
from typing import Optional
from routes.commandes import router  # Assure-toi que ce router est bien configuré

app = FastAPI()
app.include_router(router, prefix="/commandes")

client = TestClient(app)

def test_api_create_and_get_commande():
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

def test_api_commande_not_found():
    response = client.get("/commandes/9999")
    assert response.status_code == 404

def test_create_commande_duplicate_id():
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

def test_delete_commande():
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
def test_get_all_commandes():
    # Crée 2 commandes
    client.post("/commandes/", json={"id": 200, "client_id": 1, "quantite_total": 1, "montant_total": 50.0})
    client.post("/commandes/", json={"id": 201, "client_id": 2, "quantite_total": 2, "montant_total": 100.0})
    response = client.get("/commandes/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 2  # au moins 2 commandes

def test_update_commande():
    # Crée une commande
    client.post("/commandes/", json={"id": 300, "client_id": 1, "quantite_total": 1, "montant_total": 50.0})
    updated = {"id": 300, "client_id": 1, "quantite_total": 5, "montant_total": 250.0}
    response = client.put("/commandes/300", json=updated)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["quantite_total"] == 5

def test_update_commande_not_found():
    updated = {"id": 9999, "client_id": 1, "quantite_total": 5, "montant_total": 250.0}
    response = client.put("/commandes/9999", json=updated)
    assert response.status_code == 404

def test_delete_commande_not_found():
    response = client.delete("/commandes/9999")
    assert response.status_code == 404

@pytest.mark.parametrize("bad_data", [
    {"id": "bad", "client_id": 1, "quantite_total": 1, "montant_total": 100.0},
    {"id": -1, "client_id": 1, "quantite_total": 1, "montant_total": 100.0},
    {"id": 1, "client_id": 0, "quantite_total": 1, "montant_total": 100.0},
    {"id": 2, "client_id": 1, "quantite_total": 0, "montant_total": 100.0},
    {"id": 3, "client_id": 1, "quantite_total": 1, "montant_total": -5.0}
])
def test_create_commande_invalid_data(bad_data):
    response = client.post("/commandes/", json=bad_data)
    assert response.status_code == 422
def test_update_commande_success():
    data = {"id": 200, "client_id": 1, "quantite_total": 2, "montant_total": 100.0}
    client.post("/commandes/", json=data)

    updated_data = {"id": 200, "client_id": 1, "quantite_total": 5, "montant_total": 250.0}
    response = client.put("/commandes/200", json=updated_data)
    assert response.status_code == 200
    assert response.json()["quantite_total"] == 5

def test_create_commande_invalid_quantite():
    bad_data = {"id": 300, "client_id": 1, "quantite_total": 0, "montant_total": 100.0}
    response = client.post("/commandes/", json=bad_data)
    assert response.status_code == 422


def test_create_commande_invalid_montant():
    bad_data = {"id": 301, "client_id": 1, "quantite_total": 1, "montant_total": -50.0}
    response = client.post("/commandes/", json=bad_data)
    assert response.status_code == 422

def test_delete_then_delete_again():
    data = {"id": 600, "client_id": 1, "quantite_total": 2, "montant_total": 100.0}
    client.post("/commandes/", json=data)
    response = client.delete("/commandes/600")
    assert response.status_code == 200

    # Suppression à nouveau doit renvoyer 404
    response = client.delete("/commandes/600")
    assert response.status_code == 404
def test_get_commande_invalid_id_type():
    response = client.get("/commandes/bad_id")
    assert response.status_code == 422
