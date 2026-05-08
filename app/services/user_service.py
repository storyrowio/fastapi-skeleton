from typing import Optional, Any

from sqlalchemy import ColumnElement
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models import User, UserRole
from app.repositories.user_repository import UserRepository, user_repository
from app.schemas import UserFilterQuery
from app.schemas.user_schema import UserRequestSchema


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def get_all(
            self,
            db: AsyncSession,
            page: int = 1,
            limit: int = 100,
            sort_by: Optional[str] = None,
            sort_order: Optional[str] = None,
            search: Optional[str] = None,
            filter: Optional[UserFilterQuery] = None):

        skip = (page - 1) * limit

        return self.repository.get_all(
            db,
            skip=skip,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            search=search,
            filter=filter)

    def create(self, db: AsyncSession, *, obj_in: UserRequestSchema):
        return self.repository.create(db, obj_in=obj_in)

    def get_one(self, db: AsyncSession, column: ColumnElement[User], value: Any):
        return self.repository.get_one(db, column=column, value=value)

    def update(self, db: AsyncSession, db_obj: User, obj_in: UserRequestSchema | dict[Any, Any]):
        return self.repository.update(db, db_obj=db_obj, obj_in=obj_in)

    def delete(self, db: AsyncSession, id: str):
        return self.repository.delete(db, id=id)


user_service = UserService(user_repository)