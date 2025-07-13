from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from uuid import UUID
from typing import List

from api.v1.models.event import Event
from api.v1.models.rsvp import RSVP, RSVPStatus
from api.v1.schemas.rsvp import RSVPCreate, RSVPResponse
from api.v1.services.auth import get_db, get_current_user
from api.v1.models.user import User
from api.v1.services.rsvp_service import RSVPService
from api.utils import email_utils

rsvp_router = APIRouter(prefix="/rsvp", tags=["RSVP"])


@rsvp_router.post("/", response_model=RSVPResponse)
async def create_or_update_rsvp(
    data: RSVPCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await RSVPService.create_or_update_rsvp(data, current_user, db)


@rsvp_router.get("/event/{event_id}", response_model=List[RSVPResponse])
async def get_event_rsvps(
    event_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await RSVPService.get_event_rsvps(event_id, db, current_user)


@rsvp_router.get("/my", response_model=List[RSVPResponse])
async def get_my_rsvps(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await RSVPService.get_my_rsvps(current_user, db)


@rsvp_router.post("/event/{event_id}/notify")
async def notify_event_rsvps(
    event_id: UUID,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    event = await db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if event.organizer_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to notify RSVP users")

    result = await db.execute(
        select(RSVP)
        .options(selectinload(RSVP.user))
        .where(RSVP.event_id == event_id, RSVP.status.in_([RSVPStatus.attending, RSVPStatus.maybe]))
    )
    rsvps = result.scalars().all()

    if not rsvps:
        return {"message": "No RSVPs to notify"}

    subject = f"Reminder: {event.title} is coming up!"
    for rsvp in rsvps:
        email = rsvp.user.email
        html_content = f"""
        <html>
            <body>
                <h2>Reminder: You're invited to {event.title}</h2>
                <p>Date & Time: {event.start_time.strftime('%Y-%m-%d %H:%M')}</p>
                <p>Location: {event.location}</p>
                <p>We hope to see you there!</p>
            </body>
        </html>
        """
        background_tasks.add_task(
            email_utils.send_email_reminder,
            to_email=email,
            subject=subject,
            content=html_content
        )

    return {"message": f"Notification sent to {len(rsvps)} RSVP'd users"}
