from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID
from datetime import datetime


class GroupCreate(BaseModel):
    name: str
    description: Optional[str] = None
    is_private: Optional[bool] = False


class GroupResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    is_private: bool
    organizer_id: UUID

    class Config:
        orm_mode = True


class JoinGroupResponse(BaseModel):
    message: str


class GroupMemberResponse(BaseModel):
    id: UUID
    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


class GroupListResponse(BaseModel):
    id: UUID
    name: str
    description: Optional[str]
    is_private: bool
    organizer_id: UUID
    created_at: datetime

    class Config:
        orm_mode = True

class GroupActionResponse(BaseModel):
    message: str
