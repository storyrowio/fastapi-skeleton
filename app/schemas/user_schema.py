from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from app.models.user_model import UserRole


class LoginRequestSchema(BaseModel):
    email: str
    password: str
    profile_picture: Optional[str] = None
    social_provider: Optional[str] = None
    social_id: Optional[str] = None

class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class RegisterRequestSchema(BaseModel):
    name: str
    email: str
    password: Optional[str] = None
    role: Optional[UserRole] = None
    profile_picture: Optional[str] = None
    social_provider: Optional[str] = None
    social_id: Optional[str] = None

class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    name: str
    role: UserRole | None
    profile_picture: str | None
    social_provider: str | None
    social_id: str | None
    last_login_at: datetime | None
    created_at: datetime
    updated_at: datetime


class UserRequestSchema(BaseModel):
    name: str
    email: Optional[str] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    profile_picture: Optional[str] = None
    social_provider: Optional[str] = None
    social_id: Optional[str] = None

class UpdatePasswordRequestSchema(BaseModel):
    new_password: str


class UserFilterQuery(BaseModel):
    role: Optional[UserRole] = None