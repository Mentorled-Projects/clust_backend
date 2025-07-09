from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from api.v1.schemas.rsvp import RSVPCreate, RSVPResponse
from api.v1.services.auth import get_db, get_current_user
from api.v1.models.user import User
from api.v1.services.rsvp_service import RSVPService

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
    current_user: User = Depends(get_current_user)
):
    return await RSVPService.get_event_rsvps(event_id, db)

@rsvp_router.get("/my", response_model=List[RSVPResponse])
async def get_my_rsvps(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await RSVPService.get_my_rsvps(current_user, db)
