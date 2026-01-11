from typing import List, Optional
from fastapi import APIRouter, Depends, Query, Path, HTTPException, status
from sqlmodel import Session
from src.conf.db.database import Database
from src.models.ticket import Ticket, TicketBase, TicketPatch, TicketCreate
from src.services.ticket_service import TicketService

router = APIRouter(prefix="/tickets", tags=["tickets"])

# Dépendance pour fournir la session
def get_ticket_service() -> TicketService:
    session = Session(Database.get_engine())
    return TicketService(session)

# ---------------------------
# GET /tickets
# ---------------------------
@router.get("/", response_model=List[Ticket])
def list_tickets(service: TicketService = Depends(get_ticket_service)):
    """
    Récupérer tous les tickets
    """
    return service.list_tickets()


# ---------------------------
# GET /tickets/{ticket_id}
# ---------------------------
@router.get("/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: int = Path(..., gt=0), service: TicketService = Depends(get_ticket_service)):
    """
    Récupérer un ticket par ID
    """
    return service.get_ticket_by_id(ticket_id)


# ---------------------------
# POST /tickets
# ---------------------------
@router.post("/", response_model=Ticket, status_code=status.HTTP_201_CREATED)
def create_ticket(
    ticket_data: TicketCreate,
    user_id: int = Query(..., gt=0),
    tag_ids: Optional[List[int]] = Query(None),
    service: TicketService = Depends(get_ticket_service)
):
    """
    Créer un nouveau ticket.
    - `user_id` obligatoire
    - `tag_ids` optionnel
    """
    return service.create_ticket(ticket_data, user_id, tag_ids)


# ---------------------------
# PATCH /tickets/{ticket_id}
# ---------------------------
@router.patch("/{ticket_id}", response_model=Ticket)
def update_ticket(
    ticket_id: int = Path(..., gt=0),
    ticket_patch: TicketPatch = ...,
    user_id: Optional[int] = Query(None, gt=0),
    tag_ids: Optional[List[int]] = Query(None),
    service: TicketService = Depends(get_ticket_service)
):
    """
    Mettre à jour un ticket partiellement
    - `user_id` et `tag_ids` optionnels
    """
    return service.update_ticket(ticket_id, ticket_patch, user_id, tag_ids)


# ---------------------------
# DELETE /tickets/{ticket_id}
# ---------------------------
@router.delete("/{ticket_id}", status_code=status.HTTP_200_OK)
def delete_ticket(
    ticket_id: int = Path(..., gt=0),
    service: TicketService = Depends(get_ticket_service)
):
    """
    Supprimer un ticket par ID
    """
    success = service.delete_ticket(ticket_id)
    return {"ok": success}
