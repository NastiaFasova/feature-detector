from pydantic_settings import BaseSettings, SettingsConfigDict

"""
Database configuration module using Pydantic settings.

This module provides configuration management for database connections,
automatically loading settings from environment variables and .env files.
"""

class Settings(BaseSettings):
    """
        Database configuration settings loaded from environment variables.

        Attributes:
            DB_HOST: Database host address
            DB_PORT: Database port number (typically 5432 for PostgreSQL)
            DB_NAME: Name of the database to connect to
            DB_USER: Database username for authentication
            DB_PASSWORD: Database password for authentication
    """
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )

settings = Settings()

def get_db_url():
    """
      Generate PostgreSQL database URL for asyncpg driver.

      Constructs a database connection URL using the configured settings.
      The URL format is compatible with SQLAlchemy's async PostgreSQL driver (asyncpg).

      Returns:
          str: Database connection URL in the format:
               postgresql+asyncpg://username:password@host:port/database_name
      """
    return (f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@"
            f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}")