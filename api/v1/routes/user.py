from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.models.user import User
from api.v1.schemas.auth import UserResponse
from api.v1.services import auth as user_service
from api.db.session import get_db
from api.v1.services.auth import get_current_user
from api.v1.schemas.auth import UserUpdate
from api.v1.schemas.common import MessageResponse

user = APIRouter(prefix="/user", tags=["Users"])


@user.get("/me", response_model=UserResponse)
async def get_user_info(current_user: User = Depends(user_service.get_current_user)):
    return current_user

@user.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = await user_service.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@user.patch("/me", response_model=MessageResponse)
async def update_user_info(
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    updated = False

    if user_update.email is not None:
        current_user.email = user_update.email
        updated = True

    if user_update.first_name is not None:
        current_user.first_name = user_update.first_name
        updated = True

    if user_update.last_name is not None:
        current_user.last_name = user_update.last_name
        updated = True

    if not updated:
        raise HTTPException(status_code=400, detail="No changes provided")

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)

    return MessageResponse(message="User updated successfully")