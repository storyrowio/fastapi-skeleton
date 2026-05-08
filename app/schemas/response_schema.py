from typing import Optional, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

class PaginationSchema(BaseModel):
    total: int
    total_pages: int
    current_page: int
    skip: int
    limit: int


class ResponseSchema(BaseModel):
    status_code: int
    detail: str
    data: T
    pagination: Optional[PaginationSchema] = None