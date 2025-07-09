from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from api.v1.schemas.event import EventCreate, EventResponse
from api.v1.services.event_service import EventService
from api.v1.services.auth import get_db, get_current_user
from api.v1.models.user import User

event = APIRouter(prefix="/events", tags=["Events"])


@event.post("/", response_model=EventResponse)
async def create_event(
    data: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await EventService.create_event(data, current_user, db)


@event.get("/", response_model=List[EventResponse])
async def get_all_events(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await EventService.list_events(db)


@event.get("/{event_id}", response_model=EventResponse)
async def get_event_by_id(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await EventService.get_event(event_id, db)


@event.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: UUID,
    data: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await EventService.update_event(event_id, data, current_user, db)


@event.delete("/{event_id}")
async def delete_event(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await EventService.delete_event(event_id, current_user, db)
