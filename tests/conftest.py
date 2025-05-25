# tests/conftest.py
import asyncio
import pytest
import pytest_asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.core.database import Base, session_db
from main import app   # <-- seu ASGI app, de onde você exporta `app = create_app()`
from httpx import AsyncClient

# 1) URL do SQLite em memória
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# 2) Cria o engine de teste e uma SessionLocal personalizada
engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    future=True,
)
TestingSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


# 4) Override do dependency session_db para usar nosso TestingSessionLocal
@pytest.fixture(autouse=True)
def override_session_db():
    async def _override_session_db():
        async with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[session_db] = _override_session_db
    yield
    app.dependency_overrides.clear()

# 5) Cliente HTTP que já usa o override acima
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        yield ac
