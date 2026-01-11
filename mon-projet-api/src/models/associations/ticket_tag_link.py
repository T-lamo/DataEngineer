from sqlmodel import SQLModel, Field

class TicketTagLink(SQLModel, table=True):
    ticket_id: int = Field(
        foreign_key="ticket.id",
        primary_key=True,
        nullable=False
    )
    tag_id: int = Field(
        foreign_key="tag.id",
        primary_key=True,
        nullable=False
    )