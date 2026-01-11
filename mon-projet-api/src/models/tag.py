from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship
from src.models.user import User
from src.models.associations.ticket_tag_link import TicketTagLink


class TagBase(SQLModel):
    name: str

class TagPatch(TagBase):
    name: Optional[str] = None


class TagRead(TagBase):
    id: int


class Tag(TagBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, unique=True)

    tickets: List["Ticket"] = Relationship(
        back_populates="tags",
        link_model=TicketTagLink
    )


