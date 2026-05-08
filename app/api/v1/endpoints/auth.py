from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core import get_db
from app.core.deps import get_current_user
from app.models import User, UserRole
from app.schemas.response_schema import ResponseSchema
from app.schemas.user_schema import LoginRequestSchema, RegisterRequestSchema, UserRequestSchema, UserSchema
from app.services import user_service
from app.services.auth_service import auth_service

router = APIRouter()

@router.post("/register", response_model=ResponseSchema)
async def register(db: AsyncSession = Depends(get_db), req: RegisterRequestSchema = Body()):
    req.role = UserRole.USER

    res = await auth_service.register(db, req)

    return ResponseSchema(status_code=200, detail="Success", data=res)

@router.post("/login", response_model=ResponseSchema)
async def login(
        req: LoginRequestSchema,
    db: AsyncSession = Depends(get_db),
):
    res = await auth_service.login(db, req)

    return ResponseSchema(status_code=200, detail="Success", data=res)


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