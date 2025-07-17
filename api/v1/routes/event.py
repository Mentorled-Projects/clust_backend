from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from typing import List
from uuid import UUID

from api.v1.schemas.event import EventCreate, EventResponse
from api.v1.schemas.ticket import TicketCreate, TicketResponse
from api.v1.services.event_service import EventService
from api.v1.services.auth import get_db, get_current_user
from api.v1.models.user import User, UserRole
from api.v1.models import Ticket, Event

event = APIRouter(prefix="/events", tags=["Events"])


@event.post("/", response_model=EventResponse)
async def create_event(
    data: EventCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.organizer:
        current_user.role = UserRole.organizer
        db.add(current_user)
        await db.commit()
        await db.refresh(current_user)

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


@event.post("/{event_id}/tickets", response_model=TicketResponse)
async def create_ticket_for_event(
    event_id: UUID,
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    event_obj = await db.get(Event, event_id)
    if not event_obj:
        raise HTTPException(status_code=404, detail="Event not found")

    if event_obj.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to add tickets for this event")

    ticket = Ticket(
        event_id=event_id,
        name=ticket_data.name,
        price=ticket_data.price,
        payment_type=ticket_data.payment_type,
        event_capacity=ticket_data.event_capacity
    )

    db.add(ticket)
    try:
        await db.commit()
        await db.refresh(ticket)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Ticket creation failed due to a database constraint")

    result = await db.execute(select(Ticket).where(Ticket.event_id == event_id))
    tickets_for_event = result.scalars().all()

    if len(tickets_for_event) == 1:
        event_obj.is_published = True
        db.add(event_obj)
        await db.commit()
        await db.refresh(event_obj)

    return ticket