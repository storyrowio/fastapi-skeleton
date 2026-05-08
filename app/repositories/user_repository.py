import uuid
from typing import Optional, Any

from sqlalchemy import ColumnElement, func
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select, or_, desc

from app.models import User
from app.schemas import UserFilterQuery
from app.schemas.user_schema import UserRequestSchema, UserSchema


class UserRepository:
    def __init__(self):
        self.model = User

    async def get_all(
            self,
            db: AsyncSession,
            *,
            skip: int = 0,
            limit: int = 100,
            sort_by: Optional[str] = None,
            sort_order: Optional[str] = None,
            search: Optional[str] = None,
            filter: Optional[UserFilterQuery] = None,
    ):
        query = select(self.model)

        # Filter
        if filter.role:
            query = query.where(self.model.role == filter.role)

        if search:
            search_term = f"%{search}%"
            query = query.where(
                or_(
                    self.model.name.ilike(search_term),
                    self.model.email.ilike(search_term),
                )
            )

        if sort_by and sort_order:
            if sort_order == "desc":
                query = query.order_by(desc(sort_by))
            else:
                query = query.order_by(sort_by)
        else:
            query = query.order_by(desc(self.model.created_at))

        query = query.offset(skip).limit(limit)
        result = await db.exec(query)

        # Count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.exec(count_query)
        total_items = total_result.one()

        results = [UserSchema.model_validate(u) for u in result.all()]

        return results, total_items



    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: UserRequestSchema,
    ) -> User:
        db_obj = self.model(**obj_in.model_dump())
        db_obj.id = str(uuid.uuid4())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj


    async def get_one(
            self,
            db: AsyncSession,
            column: ColumnElement[Any] | str,
            value: Any,
    ) -> Optional[User]:
        col = getattr(self.model, column) if isinstance(column, str) else column
        query = select(self.model).where(col == value)
        result = await db.exec(query)
        return result.one_or_none()


    async def update(
            self,
            db: AsyncSession,
            db_obj: User,
            obj_in: UserRequestSchema | dict[Any, Any],
    ) -> User:
        update_data = obj_in.model_dump(exclude_unset=True) if hasattr(obj_in, 'model_dump') else obj_in

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj


    async def delete(
            self,
            db: AsyncSession,
            id: str
    ) -> bool:
        obj = select(User).where(id == self.model.id)
        if obj is None:
            return False

        await db.delete(obj)
        await db.commit()
        return True

user_repository = UserRepository()