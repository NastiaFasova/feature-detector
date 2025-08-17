from fastapi import FastAPI

from app.middleware.logging import RequestLoggingMiddleware
from app.routes import routes

app = FastAPI()
app.include_router(routes.router)
app.add_middleware(RequestLoggingMiddleware)
