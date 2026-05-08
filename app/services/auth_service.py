import http
from datetime import datetime
from http import HTTPStatus

from fastapi import HTTPException
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token
from app.models import UserRole, User
from app.repositories.user_repository import user_repository
from app.schemas.user_schema import RegisterRequestSchema, UserRequestSchema, LoginRequestSchema, LoginResponseSchema


class AuthService:
    def __init__(self):
        self.repository = user_repository

    async def register(self, db: AsyncSession, req: RegisterRequestSchema):
        password = get_password_hash(req.password)

        obj_in = UserRequestSchema(
            name=req.name,
            email=req.email,
            profile_picture=req.profile_picture
        )

        obj_in.role = UserRole.USER

        if req.social_provider and req.social_id:
            obj_in.social_provider = req.social_provider
            obj_in.social_id = req.social_id
        elif req.password:
            obj_in.password = password

        user = await self.repository.create(db, obj_in=obj_in)

        access_token = create_access_token(
            data={"user_id": user.id, "role": user.role, "email": user.email})

        refresh_token = create_refresh_token(
            data={"user_id": user.id, "email": user.email})

        return LoginResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )


    async def login(self, db: AsyncSession, req: LoginRequestSchema):
        user = await self.repository.get_one(db, User.email, req.email)
        if user is None:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect email or password")

        if not verify_password(req.password, user.password):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect email or password")

        access_token = create_access_token(
            data={"user_id": user.id, "role": user.role, "email": user.email})

        refresh_token = create_refresh_token(
            data={"user_id": user.id, "email": user.email})

        user.last_login_at = datetime.now()
        await db.commit()
        await db.refresh(user)

        response = LoginResponseSchema(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )

        return response



auth_service = AuthService()