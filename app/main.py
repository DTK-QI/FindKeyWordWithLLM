from fastapi import FastAPI
from app.core.config import settings
from app.api.endpoints import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION
)

app.include_router(router)