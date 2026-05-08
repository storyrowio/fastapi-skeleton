from fastapi import APIRouter, Depends, Body
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core import get_db
from app.core.deps import get_current_admin
from app.models import User, UserRole
from app.schemas import UserRequestSchema, UserFilterQuery
from app.schemas.response_schema import ResponseSchema
from app.services import user_service
from app.utils.pagination import build_list_pagination_response

router = APIRouter()

@router.get("/", response_model=ResponseSchema)
async def get_all(
        db: AsyncSession = Depends(get_db),
        page: int = 1,
        limit: int = 10,
        search: str | None = None,
        sort_by: str | None = None,
        sort_order: str | None = None,
        role: UserRole | None = None,
        current_admin: User = Depends(get_current_admin),
):
    filter = UserFilterQuery(role=role)

    items, total_items = await user_service.get_all(
        db,
        page=page,
        limit=limit,
        sort_by=sort_by,
        sort_order=sort_order,
        search=search,
        filter=filter)

    pagination = build_list_pagination_response(total_items, page, limit)

    return ResponseSchema(status_code=200, detail="Success", data=items, pagination=pagination)


@router.get("/{id}", response_model=ResponseSchema)
async def get_one(
        id: str,
        db: AsyncSession = Depends(get_db),
):
    item = await user_service.get_one(db, id=id)
    return ResponseSchema(status_code=200, detail="Success", data=item)

@router.post("/", response_model=ResponseSchema)
async def create(
        db: AsyncSession = Depends(get_db),
        user: UserRequestSchema = Body(...),
        current_admin: User = Depends(get_current_admin),
):
    item = await user_service.create(db, obj_in=user)
    return ResponseSchema(status_code=200, detail="Success", data=item)


@router.put("/{id}", response_model=ResponseSchema)
async def update(
        id: str,
        db: AsyncSession = Depends(get_db),
        req: UserRequestSchema = Body(...),
):
    item = await user_service.update(db, id=id, obj_in=req)
    return ResponseSchema(status_code=200, detail="Success", data=item)


@router.delete("/{id}", response_model=ResponseSchema)
async def delete(
        id: str,
        db: AsyncSession = Depends(get_db),
):
    item = await user_service.delete(db, id=id)
    return ResponseSchema(status_code=200, detail="Success", data=item)