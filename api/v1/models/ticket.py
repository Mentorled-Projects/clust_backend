from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.v1.models.base_class import BaseModel


class PaymentType(PyEnum):
    FREE = "free"
    PAID = "paid"
    DONATION = "donation"

class Ticket(BaseModel):
    __tablename__ = "tickets"

    event_id = Column(UUID(as_uuid=True), ForeignKey("events.id", ondelete="CASCADE"))
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=True)
    payment_type = Column(SQLEnum(PaymentType), nullable=False)
    event_capacity = Column(Integer, nullable=False)

    event = relationship("Event", back_populates="tickets")