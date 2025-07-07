# test_service_commande.py
import pytest
from models.commandes_model import Commandes
from services import commandes_service
from sqlmodel import Session, text
from database.engine import test_engine
from fastapi import HTTPException
from unittest.mock import patch
from routes.commandes import create_commande

@pytest.fixture(autouse=True)
def clean_commandes_table():
    with Session(test_engine) as session:
        session.exec(text("DELETE FROM commandes;"))
        session.commit()
    yield

def test_create_commande():
    commande = Commandes(id=1, client_id=1, quantite_total=2, montant_total=100.0)
    with Session(test_engine) as session:
        result = commandes_service.create_commande(commande, session)
        assert result is not None
        assert result.id == 1

def test_get_commande():
    commande = Commandes(id=2, client_id=1, quantite_total=3, montant_total=200.0)
    with Session(test_engine) as session:
        commandes_service.create_commande(commande, session)
        result = commandes_service.get_commande(2, session)
        assert result is not None
        assert result.montant_total == 200.0

def test_update_commande():
    commande = Commandes(id=3, client_id=2, quantite_total=1, montant_total=50.0)
    with Session(test_engine) as session:
        commandes_service.create_commande(commande, session)
        updated = Commandes(id=3, client_id=2, quantite_total=5, montant_total=250.0)
        result = commandes_service.update_commande(3, updated, session)
        assert result.quantite_total == 5

def test_delete_commande():
    commande = Commandes(id=4, client_id=2, quantite_total=1, montant_total=75.0)
    with Session(test_engine) as session:
        commandes_service.create_commande(commande, session)
        result = commandes_service.delete_commande(4, session)
        assert result is not None
        assert result.id == 4
        assert commandes_service.get_commande(4, session) is None

def test_tables_exist(session):
    result = session.exec(
        text("SELECT name FROM sqlite_master WHERE type='table' AND name='commandes'")
    )
    assert result.first() is not None

def test_create_commande_exception_handling():
    commande = Commandes(id=999, client_id=1, quantite_total=1, montant_total=100.0)

    with patch('services.commandes_service.create_commande', side_effect=Exception("Erreur test")):
        with Session(test_engine) as session:
            with pytest.raises(HTTPException) as exc_info:
                create_commande(commande, session)

            assert exc_info.value.status_code == 400
            assert "Erreur lors de la création" in exc_info.value.detail


from database.session import get_session

def test_get_session_function():
    sessions = list(get_session())
    assert len(sessions) == 1
    session = sessions[0]
    assert session is not None