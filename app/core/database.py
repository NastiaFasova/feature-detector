"""
Database setup and connection management using SQLAlchemy async engine.

This module configures the async database engine, session factory, and base model class
for the FastAPI application. It uses PostgreSQL with asyncpg driver for optimal
async performance.
"""
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from app.core.config import get_db_url

DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    """
        Abstract base class for all database models.
        """
    __abstract__ = True
