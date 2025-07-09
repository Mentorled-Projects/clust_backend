from pydantic import BaseModel
from datetime import datetime
from uuid import UUID


class EventCreate(BaseModel):
    title: str
    description: str
    location: str
    start_time: datetime
    end_time: datetime


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
