from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.core.database import Base, session_db
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from typing import Dict
import pytest_asyncio
from main import app
import pytest

DATABASE_URL = "sqlite+aiosqlite:///:memory:"

# ===================================================================================
# FIXTURE: Cria um banco SQLite em memória e injeta uma sessão SQLAlchemy async.
# ===================================================================================
@pytest_asyncio.fixture
async def db_session():
    """Cria banco de dados SQLite isolado para cada teste."""
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    session = async_session()
    try:
        yield session
    finally:
        await session.close()
        await engine.dispose()

# ======================================================================================
# FIXTURE: Injeta a session no app FastAPI para garantir isolamento dos dados no teste.
# ======================================================================================
@pytest.fixture
def client(db_session, monkeypatch):
    """Retorna um TestClient isolado com a sessão de banco sobrescrita."""
    def override_session_db():
        yield db_session
    app.dependency_overrides[session_db] = override_session_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

# ======================================================================================
# FUNÇÃO: Realiza login na API e valida status.
# ======================================================================================
def login(client, email: str, password: str, expect_status: int) -> Dict:
    """Tenta realizar login com email/senha e valida o status."""
    response = client.post("/auth/login", json={"email": email, "password": password})
    assert response.status_code == expect_status
    if expect_status == 200:
        return response.json()
    return {}
