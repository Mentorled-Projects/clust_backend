from fastapi import FastAPI, HTTPException, Depends, APIRouter
from fastapi_mail import FastMail, MessageSchema, MessageType
from starlette.responses import JSONResponse
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from core.config.settings import settings
from api.utils import email_utils
from api.v1.schemas.user import UserCreate
from api.v1.services import user as user_service

user = APIRouter(prefix='/user', tags=['User'])
serializer = URLSafeTimedSerializer(settings.SECRET_KEY)


@user.post("/signup")
async def signup(user: UserCreate):
    try:
        user_service.create_user(user.email, user.password, "")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    token = serializer.dumps(user.email)

    verification_link = f"{settings.VERIFICATION_BASE_URL}/user/verify/{token}"
    message = MessageSchema(
        subject="Verify your email",
        recipients=[user.email],
        body=f"Click the link to verify your email: {verification_link}",
        subtype=MessageType.html,
    )

    try:
        email_utils.send_email_reminder(user.email, "Verify your email", f"Click the link to verify your email: {verification_link}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to send verification email")

    return JSONResponse(status_code=200, content={"message": "Verification email sent"})

@user.get("/verify/{token}")
async def verify_email(token: str):
    try:
        email = serializer.loads(token, max_age=3600)
    except SignatureExpired:
        return JSONResponse(status_code=400, content={"message": "Token expired"})
    except BadSignature:
        return JSONResponse(status_code=400, content={"message": "Invalid token"})

    try:
        user_service.verify_user_email(email)
    except ValueError:
        return JSONResponse(status_code=400, content={"message": "Email not found"})

    return JSONResponse(status_code=200, content={"message": "Email verified successfully"})
