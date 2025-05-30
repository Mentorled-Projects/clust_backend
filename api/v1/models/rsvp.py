from sqlalchemy import Column, Enum, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum as SQLAlchemyEnum
import enum

from api.v1.models.base_class import BaseModel 

class RSVPStatus(str, enum.Enum):
    attending = "attending"
    maybe = "maybe"
    not_attending = "not_attending"

class RSVP(BaseModel):
    __tablename__ = "rsvps"

    user_id = Column(ForeignKey("users.id"), nullable=False)
    event_id = Column(ForeignKey("events.id"), nullable=False)
    status = Column(SQLAlchemyEnum(RSVPStatus, native_enum=False), nullable=False)

    user = relationship("User", back_populates="rsvps")
    event = relationship("Event", back_populates="rsvps")
