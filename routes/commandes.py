from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from database.session import get_session  # nouvelle fonction
from models.commandes_model import Commandes, CommandesRead, CommandesCreate
from services import commandes_service

router = APIRouter()
ERROR_COMMANDE_EXISTANTE = "Commande déjà existante"

@router.get("/", response_model=list[CommandesRead])
def get_all_commandes(session: Session = Depends(get_session)):
    return commandes_service.get_all_commandes(session)

@router.get("/{commande_id}", response_model=CommandesRead)
def get_commande(commande_id: int, session: Session = Depends(get_session)):
    commande = commandes_service.get_commande(commande_id, session)
    if not commande:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return commande

@router.post("/", status_code=201, response_model=CommandesRead)
def create_commande(commande: CommandesCreate, session: Session = Depends(get_session)):
    print(f"Création de la commande avec id={commande.id}")
    if commandes_service.get_commande(commande.id, session):
        print(ERROR_COMMANDE_EXISTANTE)
        raise HTTPException(status_code=400, detail=ERROR_COMMANDE_EXISTANTE)
    try:
        commande_obj = Commandes(**commande.model_dump())
        created = commandes_service.create_commande(commande_obj, session)
        if created is None:
            print("Echec création : commande existe peut-être déjà")
            raise HTTPException(status_code=400, detail=ERROR_COMMANDE_EXISTANTE)
        return created
    except Exception as e:
        print(f"Erreur lors de la création : {str(e)}")
        raise HTTPException(status_code=400, detail=f"Erreur lors de la création : {str(e)}")


@router.put("/{commande_id}", response_model=CommandesRead)
def update_commande(commande_id: int, commande_modifiee: CommandesCreate, session: Session = Depends(get_session)):
    updated = commandes_service.update_commande(commande_id, commande_modifiee, session)
    if not updated:
        raise HTTPException(status_code=404, detail="Commande non trouvée")
    return updated

@router.delete("/{commande_id}")
def delete_commande(commande_id: int, session: Session = Depends(get_session)):
    deleted = commandes_service.delete_commande(commande_id, session)
    if deleted:
        return {"detail": "Commande supprimée"}
    raise HTTPException(status_code=404, detail="Commande introuvable")
