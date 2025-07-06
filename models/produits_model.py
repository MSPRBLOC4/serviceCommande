from sqlmodel import SQLModel, Field
from typing import Optional


class Produits(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nom: str
    description: Optional[str] = None
    prix_unitaire: float
