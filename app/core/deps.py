from fastapi import Depends, HTTPException
from jose import jwt
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core import get_db, settings
from app.core.security import oauth2_scheme
from app.models import User, UserRole
from app.services import user_service


async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = await user_service.get_one(db, User.id, payload["user_id"])

        return user
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="Unauthorized")


async def get_current_admin(
    current_user: User = Depends(get_current_user),
):
    if current_user.role != UserRole.SYSTEM_ADMIN:
        raise HTTPException(status_code=403, detail="Forbidden")

    return current_user