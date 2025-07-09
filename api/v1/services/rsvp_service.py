from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from uuid import UUID
from api.v1.models.rsvp import RSVP, RSVPStatus
from api.v1.models.event import Event
from api.v1.models.user import User
from api.v1.schemas.rsvp import RSVPCreate
from sqlalchemy.orm import selectinload

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.v1.models.rsvp import RSVP, RSVPStatus
from api.v1.models.event import Event
from api.v1.models.user import User
from api.v1.schemas.rsvp import RSVPCreate
from uuid import UUID

class RSVPService:

    @staticmethod
    async def create_or_update_rsvp(data: RSVPCreate, user: User, db: AsyncSession) -> RSVP:
        event = await db.get(Event, data.event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")

        result = await db.execute(
            select(RSVP).where(RSVP.user_id == user.id, RSVP.event_id == data.event_id)
        )
        existing_rsvp = result.scalars().first()

        if existing_rsvp:
            existing_rsvp.status = data.status
            await db.commit()
            await db.refresh(existing_rsvp)
            return existing_rsvp

        new_rsvp = RSVP(
            user_id=user.id,
            event_id=data.event_id,
            status=data.status
        )
        db.add(new_rsvp)
        await db.commit()
        await db.refresh(new_rsvp)
        return new_rsvp

    @staticmethod
    async def get_event_rsvps(event_id: UUID, db: AsyncSession):
        result = await db.execute(
            select(RSVP)
            .options(selectinload(RSVP.user), selectinload(RSVP.event))
            .where(RSVP.event_id == event_id)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_my_rsvps(user: User, db: AsyncSession):
        result = await db.execute(
            select(RSVP)
            .options(selectinload(RSVP.event))
            .where(RSVP.user_id == user.id)
        )
        return result.scalars().all()

