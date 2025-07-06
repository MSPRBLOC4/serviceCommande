from sqlmodel import SQLModel, Session, select
from .engine import engine
from models.clients_model import Clients
from models.commandes_model import Commandes
from models.produits_model import Produits
from models.lignes_commandes_model import LignesCommandes
from .database import create_db_and_tables
from datetime import datetime

def insert_test_data():
    with Session(engine) as session:
        if not session.exec(select(Clients)).first():
            clients = [
                Clients(nom="Alice", email="alice@example.com"),
                Clients(nom="Bob", email="bob@example.com"),
            ]
            session.add_all(clients)
            session.commit()

        if not session.exec(select(Produits)).first():
            produits = [
                Produits(nom="Ordinateur", description="PC portable", prix_unitaire=999.99),
                Produits(nom="Souris", description="Souris sans fil", prix_unitaire=29.99),
                Produits(nom="Clavier", description="Clavier mécanique", prix_unitaire=89.99),
            ]
            session.add_all(produits)
            session.commit()

        if not session.exec(select(Commandes)).first():
            commande = Commandes(client_id=1, quantite_total=3, montant_total=1119.97)
            session.add(commande)
            session.commit()

        if not session.exec(select(LignesCommandes)).first():
            lignes = [
                LignesCommandes(id_commande=1, id_produit=1, quantite=1, prix_total=999.99, date=datetime.utcnow()),
                LignesCommandes(id_commande=1, id_produit=2, quantite=1, prix_total=29.99, date=datetime.utcnow()),
                LignesCommandes(id_commande=1, id_produit=3, quantite=1, prix_total=89.99, date=datetime.utcnow()),
            ]
            session.add_all(lignes)
            session.commit()

if __name__ == "__main__":
    create_db_and_tables()
    insert_test_data()
    print("Base initialisée avec succès.")
