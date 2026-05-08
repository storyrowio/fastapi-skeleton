from math import ceil

from app.schemas.response_schema import PaginationSchema


def build_list_pagination_response(
        total_items: int,
        page: int,
        limit: int
) -> PaginationSchema:
    skip = (page - 1) * limit
    total_pages = ceil(total_items / limit) if limit > 0 else 0
    current_page = (skip // limit) + 1 if limit > 0 else 1

    return PaginationSchema(
        total=total_items,
        total_pages=total_pages,
        current_page=current_page,
        skip=skip,
        limit=limit
    )