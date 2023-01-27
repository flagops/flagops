import asyncio
import pytest
# from uuid import UUID
from fastapi.testclient import TestClient
from urllib.parse import quote
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from ..api.main import app
from ..common.config import get_settings
from ..common.config import BaseSQLModel
from ..common.utils import get_db_session
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# from jose import jwt

settings = get_settings()

pg_db_username = "flagops_test_user"
pg_db_password = "flagops_test_password"
pg_db_name = "flagops_test_db"
db_url = f"postgresql+asyncpg://{pg_db_username}:{pg_db_password}@{settings.pg_db_host}:{settings.pg_db_port}/{pg_db_name}?ssl={settings.pg_db_ssl}"
engine = create_async_engine(db_url, future=True, poolclass=NullPool)
async_sessionmaker = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(BaseSQLModel.metadata.drop_all)
        await conn.run_sync(BaseSQLModel.metadata.create_all)

@pytest.fixture(autouse=True)
def recreate_db_after_test():
    asyncio.run(create_tables())

@pytest.fixture()
def client():
    # Dependency override
    async def override_get_db():
        connection = await engine.connect()
        session = async_sessionmaker(bind=connection)

        try:
            yield session
        finally:
            await session.close()
            await connection.close()

    app.dependency_overrides[get_db_session] = override_get_db

    return TestClient(app)


# class TestJWTData:
#     user_id = UUID("1e721695-e156-443c-8c2d-6cde7f7aebf6")
#     username = "test_user"
#     tenant_id = UUID("b7af8784-f8f7-416f-8d3f-d633542d925a")
#     email = "test@mail.com"

#     @classmethod
#     def get_jwt_token(cls) -> str:
#         return jwt.encode(
#             {
#                 "userId": str(cls.user_id),
#                 "username": cls.username,
#                 "tenantId": str(cls.tenant_id),
#                 "fullName": cls.username,
#                 "email": cls.email,
#             },
#             "secret",
#         )
