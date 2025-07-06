import pytest
from models.commandes_model import Commandes
from services import commandes_service
from sqlmodel import Session, text
from database.engine import engine

@pytest.fixture()
def session():
    with Session(engine) as session:
        session.exec(text("TRUNCATE TABLE commandes RESTART IDENTITY CASCADE;"))
        session.commit()
        yield session

def test_create_commande(session):
    commande = Commandes(id=1, client_id=1, quantite_total=2, montant_total=100.0)
    result = commandes_service.create_commande(commande, session)
    assert result is not None
    assert result.id == 1

def test_get_commande(session):
    commande = Commandes(id=2, client_id=1, quantite_total=3, montant_total=200.0)
    commandes_service.create_commande(commande, session)
    result = commandes_service.get_commande(2, session)
    assert result is not None
    assert result.montant_total == 200.0

def test_update_commande(session):
    commande = Commandes(id=3, client_id=2, quantite_total=1, montant_total=50.0)
    commandes_service.create_commande(commande, session)
    updated = Commandes(id=3, client_id=2, quantite_total=5, montant_total=250.0)
    result = commandes_service.update_commande(3, updated, session)
    assert result.quantite_total == 5

def test_delete_commande(session):
    commande = Commandes(id=4, client_id=2, quantite_total=1, montant_total=75.0)
    commandes_service.create_commande(commande, session)
    result = commandes_service.delete_commande(4, session)
    assert result is not None
    assert result.id == 4
    assert commandes_service.get_commande(4, session) is None
