from passlib.context import CryptContext
from api.v1.models.user import User, fake_user_db
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_user(email: str, password: str, name: Optional[str] = "") -> dict:
    if email in fake_user_db:
        raise ValueError("Email already registered")
    hashed_password = hash_password(password)
    user_data = {
        "email": email,
        "password_hash": hashed_password,
        "name": name,
        "role": "attendee",
        "verified": False
    }
    fake_user_db[email] = user_data
    return user_data

def verify_user_email(email: str):
    if email in fake_user_db:
        fake_user_db[email]["verified"] = True
    else:
        raise ValueError("Email not found")
