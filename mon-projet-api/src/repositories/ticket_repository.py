from typing import List, Optional
from sqlmodel import Session, select
from src.conf.db.database import Database
from src.models.ticket import Ticket, TicketPatch

class TicketRepository:

    @staticmethod
    def get_all_tickets() -> List[Ticket]:
        """Récupérer tous les tickets"""
        with Session(Database.get_engine()) as session:
            statement = select(Ticket)
            return session.exec(statement).all()

    @staticmethod
    def get_ticket_by_id(ticket_id: int) -> Optional[Ticket]:
        """Récupérer un ticket par ID"""
        with Session(Database.get_engine()) as session:
            return session.get(Ticket, ticket_id)

    @staticmethod
    def create_ticket(ticket: Ticket) -> Ticket:
        """Créer un nouveau ticket"""
        with Session(Database.get_engine()) as session:
            session.add(ticket)
            session.commit()
            session.refresh(ticket)
            return ticket

    @staticmethod
    def update_ticket(ticket_id: int, updated_ticket: TicketPatch) -> Optional[Ticket]:
        """Mettre à jour un ticket existant"""
        with Session(Database.get_engine()) as session:
            ticket = session.get(Ticket, ticket_id)
            if not ticket:
                return None
            for field, value in updated_ticket.dict(exclude_unset=True).items():
                setattr(ticket, field, value)
            session.add(ticket)
            session.commit()
            session.refresh(ticket)
            return ticket

    @staticmethod
    def delete_ticket(ticket_id: int) -> bool:
        """Supprimer un ticket par ID"""
        with Session(Database.get_engine()) as session:
            ticket = session.get(Ticket, ticket_id)
            if not ticket:
                return False
            session.delete(ticket)
            session.commit()
            return True
