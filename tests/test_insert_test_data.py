import pytest
from sqlalchemy import text
from sqlmodel import Session, select

from database.database import create_db_and_tables
from database.init_db import insert_test_data
from database.engine import test_engine
from models.clients_model import Clients
from models.produits_model import Produits
from models.commandes_model import Commandes
from models.lignes_commandes_model import LignesCommandes

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Crée les tables une seule fois avant la session de tests
    create_db_and_tables()
    yield
    # Ici tu peux faire un nettoyage final si tu veux

@pytest.fixture(autouse=True)
def clean_tables_before_each_test():
    # Nettoyage avant CHAQUE test pour être sûr d’avoir une DB vide
    with Session(test_engine) as session:
        session.exec(text("DELETE FROM lignesCommandes"))
        session.exec(text("DELETE FROM commandes"))
        session.exec(text("DELETE FROM produits"))
        session.exec(text("DELETE FROM clients"))
        session.commit()

def test_insert_test_data_populates_tables():
    insert_test_data()

    with Session(test_engine) as session:
        clients = session.exec(select(Clients)).all()
        produits = session.exec(select(Produits)).all()
        commandes = session.exec(select(Commandes)).all()
        lignes = session.exec(select(LignesCommandes)).all()

    assert len(clients) > 0, "Clients non insérés"
    assert len(produits) > 0, "Produits non insérés"
    assert len(commandes) > 0, "Commandes non insérées"
    assert len(lignes) > 0, "LignesCommandes non insérées"

def test_insert_test_data_covers_lignes_block():
    insert_test_data()

    with Session(test_engine) as session:
        lignes = session.exec(select(LignesCommandes)).all()
        assert len(lignes) == 3
