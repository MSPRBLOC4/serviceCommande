import pytest
from models.commandes_model import CommandesCreate
from pydantic import ValidationError

def test_commande_create_validation():
    valid = CommandesCreate(id=1, client_id=1, quantite_total=2, montant_total=100.0)
    assert valid.id == 1

    with pytest.raises(ValidationError):
        CommandesCreate(id=0, client_id=1, quantite_total=2, montant_total=100.0)

    with pytest.raises(ValidationError):
        CommandesCreate(id=2, client_id=0, quantite_total=2, montant_total=100.0)

    with pytest.raises(ValidationError):
        CommandesCreate(id=3, client_id=1, quantite_total=0, montant_total=100.0)

    with pytest.raises(ValidationError):
        CommandesCreate(id=4, client_id=1, quantite_total=2, montant_total=0.0)
