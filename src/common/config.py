from sqlalchemy import Column
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, sessionmaker
from functools import lru_cache
from pydantic import BaseSettings

class Settings(BaseSettings):
    pg_db_host: str
    pg_db_port: str
    pg_db_name: str
    pg_db_username: str
    pg_db_password: str
    pg_db_ssl: str
    jwks_url: str

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings()->Settings:
    return Settings()

@lru_cache()
def get_db_url(asynchronous=False)->str:
    settings = get_settings()
    driver = "psycopg2" if not asynchronous else "asyncpg"
    sslmode_key = "sslmode" if not asynchronous else "ssl"
    return f"postgresql+{driver}://{settings.pg_db_username}:{settings.pg_db_password}@{settings.pg_db_host}:{settings.pg_db_port}/{settings.pg_db_name}?{sslmode_key}={settings.pg_db_ssl}"

engine = create_async_engine(get_db_url(asynchronous=True), future=True)
async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

BaseModel = declarative_base()

class BaseSQLModel(BaseModel):
    tenant_id = Column(UUID(as_uuid=True), nullable=False)

    __abstract__ = True

# BaseSQLModel = declarative_base()


JWT_DECODE_OPTIONS = {"verify_exp": True, "verify_aud": False}
