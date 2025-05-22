from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from typing import Optional

from api.v1.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def get_user_by_email(email: str, db: AsyncSession):
    stmt = select(User).where(User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(email: str, hashed_password: str, db: AsyncSession, name: Optional[str] = "") -> User:
    result = await db.execute(select(User).where(User.email == email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise ValueError("Email already registered")

    new_user = User(
        email=email,
        password_hash=hashed_password,
        name=name,
        role="attendee",
        is_verified=False
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def verify_user_email(email: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        raise ValueError("User not found")

    user.is_verified = True
    await db.commit()
    await db.refresh(user)
    return user
