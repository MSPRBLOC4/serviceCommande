from sqlmodel import SQLModel, Field
from typing import Optional



class CommandesBase(SQLModel):
    client_id: int = Field(..., gt=0)
    quantite_total: int = Field(..., ge=1)
    montant_total: float = Field(..., ge=0.01)


class CommandesCreate(CommandesBase):
    id: int = Field(..., gt=0)


class CommandesRead(CommandesBase):
    id: int


class Commandes(CommandesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)