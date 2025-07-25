from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, model_validator, ValidationError
from typing import Optional
from typing import Literal

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    password_verify: str
    first_name: str
    last_name: str

    @model_validator(mode="before")
    def passwords_match(cls, values):
        password = values.get("password")
        password_verify = values.get("password_verify")
        if password != password_verify:
            raise ValueError("passwords do not match")
        return values

class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    is_verified: bool
    role: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=2, max_length=20)
    last_name: Optional[str] = Field(None, min_length=2, max_length=20)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class UserInfo(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    role: str
    is_verified: bool
    
class LoginResponse(BaseModel):
    message: str
    access_token: str
    token_type: Literal["bearer"]
    user: UserInfo

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LogoutRequest(BaseModel):
    access_token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr


class TokenVerifyRequest(BaseModel):
    token: str
class PasswordResetVerify(BaseModel):
    token: str
    new_password: str
    new_password_verify: str

    @model_validator(mode="before")
    def passwords_match(cls, values):
        if values["new_password"] != values["new_password_verify"]:
            raise ValueError("Passwords do not match")
        return values
    

class ResendVerificationRequest(BaseModel):
    email: EmailStr


# class EmailVerificationRequest(BaseModel):
#     email: str
#     token: str