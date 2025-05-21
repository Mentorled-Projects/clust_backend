from fastapi import FastAPI, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from core.config.settings import settings
from api.utils import email_utils
from api.v1.schemas.auth import UserCreate, UserResponse
from api.v1.services import user as user_service
from api.db.session import get_db
from api.utils.password import hash_passsword

user = APIRouter(prefix="/user", tags=["User"])
serializer = URLSafeTimedSerializer(settings.SECRET_KEY)

@user.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = await user_service.get_user_by_email(user_data.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if not user_service.verify_user_email(user_data.email, db):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Optional: Add your own password complexity check here instead of verify_password
    if len(user_data.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

    # Hash the password
    hashed_password = user_service.hash_password(user_data.password)

    try:
        await user_service.create_user(user_data.email, hashed_password, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = serializer.dumps(user_data.email)
    verification_link = f"{settings.VERIFICATION_BASE_URL}/user/verify/{token}"

    try:
        email_utils.send_email_reminder(
            to_email=user_data.email,
            subject="Verify your email",
            content=f"Click the link to verify your email: {verification_link}"
        )
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to send verification email")

    return JSONResponse(status_code=200, content={"message": "Verification email sent"})


@user.get("/verify/{token}")
async def verify_email(token: str, db: Session = Depends(get_db)):
    try:
        email = serializer.loads(token, max_age=3600)
    except SignatureExpired:
        return JSONResponse(status_code=400, content={"message": "Token expired"})
    except BadSignature:
        return JSONResponse(status_code=400, content={"message": "Invalid token"})

    try:
        await user_service.verify_user_email(email, db)
    except ValueError:
        return JSONResponse(status_code=400, content={"message": "Email not found"})

    return JSONResponse(status_code=200, content={"message": "Email verified successfully"})
