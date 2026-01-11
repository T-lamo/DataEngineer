from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from src.models.user import User
from src.models.associations.ticket_tag_link import TicketTagLink


class TicketBase(SQLModel):
    title: str
    description: Optional[str] = None


class TicketPatch(TicketBase):
    title: Optional[str] = None
    description: Optional[str] = None


class TicketCreate(TicketBase):
    pass    


class Ticket(TicketBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="user.id", nullable=False)

    user: Optional[User] = Relationship(back_populates="tickets")
    tags: List["Tag"] = Relationship(
        back_populates="tickets",
        link_model=TicketTagLink
    )
