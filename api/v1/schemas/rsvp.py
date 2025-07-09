from pydantic import BaseModel
from uuid import UUID
from enum import Enum
from datetime import datetime


class RSVPStatus(str, Enum):
    attending = "attending"
    maybe = "maybe"
    not_attending = "not_attending"


class RSVPCreate(BaseModel):
    event_id: UUID
    status: RSVPStatus


class RSVPResponse(BaseModel):
    id: UUID
    event_id: UUID
    user_id: UUID
    status: RSVPStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
