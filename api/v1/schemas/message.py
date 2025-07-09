from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class MessageCreate(BaseModel):
    content: str


class SenderResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

        
class MessageResponse(BaseModel):
    id: UUID
    content: str
    sender: SenderResponse
    sender_id: UUID
    group_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

