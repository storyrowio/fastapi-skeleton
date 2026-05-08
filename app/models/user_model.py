import enum
from datetime import datetime
from typing import List, Optional

from sqlalchemy import Enum as SAEnum, Column
from sqlmodel import SQLModel, Field, Relationship

class UserRole(str, enum.Enum):
    SYSTEM_ADMIN = "SYSTEM_ADMIN"
    USER = "USER"


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: str = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=100)
    email: str
    password: str = Field(min_length=3, max_length=100)
    role: UserRole = Field(default=UserRole.USER, sa_column=Column(SAEnum(UserRole, native_enum=False)))
    profile_picture: str | None = Field(default=None)
    social_provider: str | None = Field(default=None)
    social_id: str | None = Field(default=None)
    last_login_at: datetime | None = Field(default=None)

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)