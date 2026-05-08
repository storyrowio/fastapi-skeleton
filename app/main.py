from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 App starting...")

    yield

    print("🛑 App shutting down...")


app = FastAPI(
    title=settings.APP_TITLE,
)

app.add_middleware(CORSMiddleware)

app.include_router(api_router, prefix=settings.API_V1_STR)