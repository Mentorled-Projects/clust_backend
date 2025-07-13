from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from api.v1.services.auth import get_db, get_current_user
from api.v1.models.user import User
from api.v1.schemas.message import MessageCreate, MessageResponse
from api.v1.services.message_service import MessageService

message = APIRouter(prefix="/message", tags=["Messages"])

@message.post("/{group_id}/messages", response_model=MessageResponse)
async def send_message(
    group_id: UUID,
    data: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await MessageService.send_message(group_id, current_user, data, db)

@message.post("/{group_id}/messages", response_model=MessageResponse)
async def get_messages(
    group_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await MessageService.get_group_messages(group_id, current_user, db)
