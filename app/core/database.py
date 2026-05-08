import ssl

from sqlalchemy import make_url
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from typing_extensions import AsyncGenerator

from app.core.config import settings

url = make_url(settings.DATABASE_URL)

query = dict(url.query)
query.pop("sslmode", None)

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

engine = create_async_engine(
    url.set(query=query),
    future=True,
    echo=True,
    connect_args={"ssl": ssl_context})
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()