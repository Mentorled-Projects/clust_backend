from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID
from .ticket import TicketCreate


class EventCreate(BaseModel):
    title: str
    description: str
    location: str
    start_time: datetime
    end_time: datetime
    tickets: Optional[List[TicketCreate]] = None


class EventResponse(BaseModel):
    id: UUID
    title: str
    description: str
    location: str
    start_time: datetime
    end_time: datetime
    organizer_id: UUID

    class Config:
        orm_mode = True
