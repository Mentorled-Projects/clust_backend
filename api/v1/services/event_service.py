from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from uuid import UUID
from typing import List

from api.v1.models.event import Event
from api.v1.models.user import User
from api.v1.schemas.event import EventCreate


class EventService:
    @staticmethod
    async def create_event(data: EventCreate, user: User, db: AsyncSession) -> Event:
        new_event = Event(
            title=data.title,
            description=data.description,
            location=data.location,
            start_time=data.start_time,
            end_time=data.end_time,
            organizer_id=user.id
        )
        db.add(new_event)
        await db.commit()
        await db.refresh(new_event)
        return new_event

    @staticmethod
    async def list_events(db: AsyncSession) -> List[Event]:
        result = await db.execute(select(Event))
        return result.scalars().all()

    @staticmethod
    async def get_event(event_id: UUID, db: AsyncSession) -> Event:
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        return event

    @staticmethod
    async def update_event(event_id: UUID, data: EventCreate, user: User, db: AsyncSession) -> Event:
        event = await db.get(Event, event_id)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        if event.organizer_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You are not authorized to edit this event. Only the organizer can update it."
            )

        for key, value in data.dict().items():
            setattr(event, key, value)

        await db.commit()
        await db.refresh(event)

        return event


    @staticmethod
    async def delete_event(event_id: UUID, user: User, db: AsyncSession):
        event = await db.get(Event, event_id)
        if not event:
            raise HTTPException(status_code=404, detail="Event not found")
        if event.organizer_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized")
        await db.delete(event)
        await db.commit()
        return {"detail": "Event deleted"}
