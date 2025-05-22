from fastapi import FastAPI, HTTPException, Depends, APIRouter, Request, status
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from sqlalchemy import select


from core.config.settings import settings
from api.utils import email_utils
from api.v1.schemas.auth import UserCreate, UserResponse, LoginRequest, Token
from api.v1.services import auth as user_service
from api.db.session import get_db
from api.utils.auth import hash_passsword, validate_password, verify_password, validate_email_format, create_access_token
from api.v1.models.user import User
from api.utils.token import oauth2_scheme

user = APIRouter(prefix="/user", tags=["Auth"])
serializer = URLSafeTimedSerializer(settings.SECRET_KEY)


@user.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    validate_password(user_data.password)
    validate_email_format(user_data.email)

    existing_user = await user_service.get_user_by_email(user_data.email, db)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    

    if len(user_data.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

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

    db.commit()
    return JSONResponse(status_code=200, content={"message": "Email verified successfully"})


@user.post("/login")
async def login(user_data: LoginRequest, db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == user_data.email)
    result = await db.execute(stmt)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_verified:
        raise HTTPException(status_code=403, detail="Please verify your email before logging in")

    # TODO: generate and return token or session
    return {"message": "Login successful"}

@user.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    await user_service.blacklist_token(token)
    return {"detail": "Logged out successfully"}