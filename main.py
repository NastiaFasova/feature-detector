from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import engine, Base
from app.middleware.logging import RequestLoggingMiddleware
from app.routes import routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.include_router(routes.router)
app.add_middleware(RequestLoggingMiddleware)
