from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.v1.models.user import User
from api.v1.schemas.auth import UserResponse
from api.v1.services import auth as user_service
from api.db.session import get_db
from api.v1.services.auth import get_current_user, pwd_context
from api.v1.schemas.auth import UserUpdate

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

@user.patch("/me", response_model=dict)
async def update_user_info(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    user = current_user
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated = False

    if user_update.email is not None:
        user.email = user_update.email
        updated = True

    if user_update.first_name is not None:
        user.first_name = user_update.first_name
        updated = True

    if user_update.last_name is not None:
        user.last_name = user_update.last_name
        updated = True

    if updated:
        db.add(current_user)
        await db.commit()
        await db.refresh(user)
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=400, detail="No changes provided")
