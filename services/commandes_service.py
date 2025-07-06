import pytest
from sqlmodel import Session, SQLModel, create_engine
from models.commandes_model import Commandes
from services import commandes_service

@pytest.fixture()
def session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

def test_create_and_get_commande(session):
    cmd = Commandes(id=1, client_id=1, quantite_total=3, montant_total=150.0)
    created = commandes_service.create_commande(cmd, session)
    assert created is not None
    assert created.id == 1

    fetched = commandes_service.get_commande(1, session)
    assert fetched is not None
    assert fetched.montant_total == 150.0

def test_update_commande(session):
    cmd = Commandes(id=2, client_id=1, quantite_total=1, montant_total=50.0)
    commandes_service.create_commande(cmd, session)

    update_data = Commandes(id=2, client_id=1, quantite_total=5, montant_total=250.0)
    updated = commandes_service.update_commande(2, update_data, session)
    assert updated.quantite_total == 5

def test_delete_commande(session):
    cmd = Commandes(id=3, client_id=1, quantite_total=2, montant_total=100.0)
    commandes_service.create_commande(cmd, session)

    deleted = commandes_service.delete_commande(3, session)
    assert deleted is not None
    assert commandes_service.get_commande(3, session) is None
