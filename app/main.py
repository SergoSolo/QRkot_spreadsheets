from fastapi import FastAPI

from app.api.routers import main_router
from app.core.config import configure_logging, settings
from app.core.init_db import create_first_superuser

app = FastAPI(title=settings.app_title, description=settings.description)

app.include_router(main_router)


@app.on_event('startup')
async def startup():
    configure_logging()
    await create_first_superuser()
