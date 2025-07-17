from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from api.db.session import get_db
from api.v1.models import Category, User
from api.v1.schemas.category import CategoryOut, CategoryAssign
from api.v1.services.auth import get_current_user

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/", response_model=list[CategoryOut])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Category))
    return result.scalars().all()

@router.post("/assign", status_code=204)
async def assign_categories_to_user(
    payload: CategoryAssign,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not current_user:
        raise HTTPException(status_code=401, detail="Unauthorized")

    result = await db.execute(select(Category).where(Category.id.in_(payload.category_ids)))
    selected = result.scalars().all()

    if len(selected) != len(payload.category_ids):
        raise HTTPException(status_code=400, detail="One or more categories not found")

    current_user.categories = selected
    await db.commit()

