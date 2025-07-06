from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class LignesCommandes(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    id_produit: Optional[int] = Field(default=None, foreign_key="produits.id")
    id_commande: Optional[int] = Field(default=None, foreign_key="commandes.id")
    quantite: Optional[int] = Field(default=None)
    prix_total: Optional[float] = Field(default=None)
    date: datetime = Field(default_factory=datetime.utcnow)
