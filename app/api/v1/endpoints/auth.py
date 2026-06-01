import os

from fastapi import APIRouter, Depends, Body
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core import get_db
from app.core.config import settings
from app.core.deps import get_current_user
from app.models import User, UserRole
from app.schemas.response_schema import ResponseSchema
from app.schemas.user_schema import LoginRequestSchema, RegisterRequestSchema, UserRequestSchema, UserSchema
from app.services import user_service
from app.services.auth_service import auth_service

router = APIRouter()


def _set_auth_cookies(response: JSONResponse, access_token: str, refresh_token: str) -> None:
    """Set access_token and refresh_token as HttpOnly cookies on the response."""
    secure = os.getenv("APP_ENV", "development") != "development"

    access_token_max_age = settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    refresh_token_max_age = settings.REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60

    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=access_token_max_age,
        path="/",
        secure=secure,
        httponly=True,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=refresh_token_max_age,
        path="/",
        secure=secure,
        httponly=True,
        samesite="lax",
    )


@router.post("/register", response_model=ResponseSchema)
async def register(db: AsyncSession = Depends(get_db), req: RegisterRequestSchema = Body()):
    req.role = UserRole.USER

    res = await auth_service.register(db, req)

    body = ResponseSchema(status_code=200, detail="Success", data=res)
    response = JSONResponse(status_code=200, content=body.model_dump())
    _set_auth_cookies(response, res.access_token, res.refresh_token)
    return response


@router.post("/login", response_model=ResponseSchema)
async def login(
    req: LoginRequestSchema,
    db: AsyncSession = Depends(get_db),
):
    res = await auth_service.login(db, req)

    body = ResponseSchema(status_code=200, detail="Success", data=res)
    response = JSONResponse(status_code=200, content=body.model_dump())
    _set_auth_cookies(response, res.access_token, res.refresh_token)
    return response


@router.get("/me", response_model=ResponseSchema)
async def me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ResponseSchema(status_code=200, detail="Success", data=UserSchema.model_validate(current_user, from_attributes=True))


@router.put("/me", response_model=ResponseSchema)
async def update_me(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    req: UserRequestSchema = Body(),
):
    res = await user_service.update(db, db_obj=current_user, obj_in=req)

    return ResponseSchema(status_code=200, detail="Success", data=UserSchema.model_validate(res, from_attributes=True))