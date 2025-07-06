from sqlmodel import Session, select
from models.commandes_model import Commandes
from database import session

def get_all_commandes(session: Session):
    return session.exec(select(Commandes)).all()

def get_commande(commande_id: int, session: Session):
    return session.get(Commandes, commande_id)

def create_commande(commande: Commandes, session: Session):
    existing = session.get(Commandes, commande.id)
    if existing:
        return None
    session.add(commande)
    session.commit()
    session.refresh(commande)
    return commande

def update_commande(commande_id: int, commande_modifiee: Commandes, session: Session):
    commande = session.get(Commandes, commande_id)
    if commande:
        commande.client_id = commande_modifiee.client_id
        commande.quantite_total = commande_modifiee.quantite_total
        commande.montant_total = commande_modifiee.montant_total
        session.commit()
        session.refresh(commande)
        return commande
    return None

def delete_commande(commande_id: int, session: Session):
    commande = session.get(Commandes, commande_id)
    if commande:
        session.delete(commande)
        session.commit()
        return commande
    return None
