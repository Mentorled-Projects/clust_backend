from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.v1.models.group import Group
from sqlalchemy.orm import selectinload
from api.v1.models.message import Message
from api.v1.models.user import User
from api.v1.schemas.message import MessageCreate
from uuid import UUID
from typing import List


class MessageService:
    @staticmethod
    async def send_message(group_id: UUID, user: User, data: MessageCreate, db: AsyncSession) -> Message:
        result = await db.execute(
            select(Group).options(selectinload(Group.members)).where(Group.id == group_id)
        )
        group = result.scalar_one_or_none()

        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        if user not in group.members:
            raise HTTPException(status_code=403, detail="You are not a member of this group.")

        if not data.content.strip():
            raise HTTPException(status_code=400, detail="Message content cannot be empty.")

        message = Message(
            content=data.content,
            sender_id=user.id,
            group_id=group_id
        )
        db.add(message)
        await db.commit()
        await db.refresh(message)

        result = await db.execute(
            select(Message)
            .options(selectinload(Message.sender))
            .where(Message.id == message.id)
        )
        return result.scalar_one()

    @staticmethod
    async def get_group_messages(group_id: UUID, user: User, db: AsyncSession) -> List[Message]:
        result = await db.execute(
            select(Group).options(selectinload(Group.members)).where(Group.id == group_id)
        )
        group = result.scalar_one_or_none()

        if not group:
            raise HTTPException(status_code=404, detail="Group not found")

        if user not in group.members:
            raise HTTPException(status_code=403, detail="You are not a member of this group.")

        result = await db.execute(
            select(Message)
            .options(selectinload(Message.sender))
            .where(Message.group_id == group_id)
            .order_by(Message.created_at)
        )
        return result.scalars().all()