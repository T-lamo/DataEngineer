from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status

from src.models.ticket import Ticket, TicketPatch, TicketBase, TicketCreate
from src.models.user import User
from src.models.tag import Tag
from src.repositories.ticket_repository import TicketRepository
from src.repositories.user_repository import UserRepository
from src.repositories.tag_repository import TagRepository  # si tu as un repo Tag


class TicketService:
    def __init__(self, session: Session):
        self.repo = TicketRepository()
        self.user_repo = UserRepository()
        self.tag_repo = TagRepository()
        self.session = session

    def list_tickets(self) -> List[Ticket]:
        """Récupérer tous les tickets"""
        with self.session as session:
            return self.repo.get_all_tickets()

    def get_ticket_by_id(self, ticket_id: int) -> Ticket:
        """Récupérer un ticket par ID"""
        with self.session as session:
            ticket = self.repo.get_ticket_by_id(ticket_id)
            if not ticket:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ticket with ID {ticket_id} not found"
                )
            return ticket

    def create_ticket(self, ticket_data: TicketCreate, user_id: int, tag_ids: Optional[List[int]] = None) -> Ticket:
        """Créer un ticket avec validations"""
        with self.session as session:
            # Vérifier que l'utilisateur existe
            user = self.user_repo.get_user_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"User with ID {user_id} not found"
                )

            # Vérifier la validité du titre
            if not ticket_data.title or ticket_data.title.strip() == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ticket title is required"
                )

            # Vérifier les tags existants si fournis
            tags = []
            if tag_ids:
                for tag_id in tag_ids:
                    tag = self.tag_repo.get_tag_by_id(tag_id)
                    if not tag:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tag with ID {tag_id} not found"
                        )
                    tags.append(tag)

            ticket = Ticket(
                title=ticket_data.title.strip(),
                description=ticket_data.description,
                user_id=user_id,
                tags=tags
            )

            return self.repo.create_ticket(ticket)

    def update_ticket(self, ticket_id: int, ticket_patch: TicketPatch, user_id: Optional[int] = None, tag_ids: Optional[List[int]] = None) -> Ticket:
        """Mettre à jour un ticket avec validations"""
        with self.session as session:
            ticket = self.repo.get_ticket_by_id(ticket_id)
            if not ticket:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ticket with ID {ticket_id} not found"
                )

            # Validation du titre si fourni
            if ticket_patch.title is not None and ticket_patch.title.strip() == "":
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ticket title cannot be empty"
                )

            # Validation de l'utilisateur si fourni
            if user_id is not None:
                user = self.user_repo.get_user_by_id(user_id)
                if not user:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with ID {user_id} not found"
                    )
                ticket.user_id = user_id

            # Validation des tags si fournis
            if tag_ids is not None:
                tags = []
                for tag_id in tag_ids:
                    tag = self.tag_repo.get_tag_by_id(tag_id)
                    if not tag:
                        raise HTTPException(
                            status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Tag with ID {tag_id} not found"
                        )
                    tags.append(tag)
                ticket.tags = tags

            # Mise à jour partielle des champs Ticket
            for field, value in ticket_patch.dict(exclude_unset=True).items():
                setattr(ticket, field, value)

            return self.repo.update_ticket(ticket_id, ticket)

    def delete_ticket(self, ticket_id: int) -> bool:
        """Supprimer un ticket avec validation"""
        with self.session as session:
            success = self.repo.delete_ticket(ticket_id)
            if not success:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ticket with ID {ticket_id} not found"
                )
            return True
