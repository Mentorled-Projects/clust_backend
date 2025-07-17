from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, model_validator
from uuid import UUID

class PaymentType(str, Enum):
    FREE = "free"
    PAID = "paid"
    DONATION = "donation"

class TicketCreate(BaseModel):
    name: str = Field(..., max_length=100)
    price: Optional[float] = None
    payment_type: PaymentType
    event_capacity: int = Field(..., gt=0)

    @model_validator(mode="after")
    def validate_price_based_on_payment_type(self) -> "TicketCreate":
        if self.payment_type == PaymentType.PAID:
            if self.price is None or self.price <= 0:
                raise ValueError("Price must be a positive number for paid tickets.")
        elif self.payment_type == PaymentType.DONATION:
            if self.price is None or self.price < 0:
                raise ValueError("Price must be 0 or more for donation-based tickets.")
        elif self.payment_type == PaymentType.FREE:
            if self.price is not None:
                raise ValueError("Price must not be set for free tickets.")
        return self

class TicketResponse(BaseModel):
    id: UUID
    event_id: UUID
    name: str
    payment_type: PaymentType
    price: Optional[float]
    event_capacity: int

    class Config:
        orm_mode = True
