from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from app.repositories import BaseRepository
from app.utils.fecth_by_id_or_404 import fecth_by_id_or_404
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
# BLOCO AUXILIAR: Cria usuários direto no banco para preparar o teste.
# ======================================================================================
async def create_user_in_db(db_session, username, email, password, is_admin):
    """Cria usuário no banco direto (usado para seed do teste)."""
    from app.models.users import UserModel
    from app.services.users import UserService
    
    user = await BaseRepository(db_session, UserModel).get_by_field("email", email)
    if user:
        return user
    
    user = UserModel(
        username=username,
        email=email,
        hashed_password=UserService(None).hash_password(password),
        is_admin=is_admin,
        is_active=True
    )
    
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user


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


async def get_token(client, db_session, is_admin=True):
    # Cria usuário admin, caso ainda não exista
    await create_user_in_db(db_session, "admin", "admin@email.com", "adminpass", is_admin=is_admin)
    token = login(client, email="admin@email.com", password="adminpass", expect_status=200)["token"]["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def create_item(client, db_session, route: str, body: Dict, expect_status: int):
    headers = await get_token(client, db_session, False)
    response = client.post(route, json=body, headers=headers)
    assert response.status_code == expect_status, response.text
    return response

# ======================================================================================
# BLOCO AUXILIAR: Cria usuários direto no banco para preparar o teste.
# ======================================================================================
async def create_item_in_db(db_session, model, data):
    """Cria usuário no banco direto (usado para seed do teste)."""
    data_model = model(**data)
    return await BaseRepository(db_session, model).create(data_model)

# @pytest_asyncio.fixture
# async def auth_client():
#     async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
#         # Registra e loga o usuário admin (ajuste se necessário para seu sistema)
#         await ac.post("/auth/register", json={
#             "username": "admin",
#             "email": "admin@email.com",
#             "password": "admin123",
#             "is_admin": True
#         })
#         resp = await ac.post("/auth/login", json={
#             "email": "admin@email.com",
#             "password": "admin123"
#         })
#         access_token = resp.json()["token"]["access_token"]
#         ac.headers = {"Authorization": f"Bearer {access_token}"}
#         yield ac