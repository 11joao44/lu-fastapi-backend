import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient

BASE_URL = "http://127.0.0.1:8000"

# -----------------------
# Helpers para unicidade
# -----------------------
def make_unique_user():
    unique = uuid.uuid4().hex[:8]
    return {
        "username": f"user_{unique}",
        "email": f"{unique}@test.com",
        "password": "senha123"
    }

def make_admin():
    return {
        "username": "admin",
        "email": "admin@email.com",
        "password": "admin123",
        "is_admin": True
    }

# -----------------------
# Fixture para client NÃO autenticado (só use no primeiro user!)
# -----------------------
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url=BASE_URL) as ac:
        yield ac

# -----------------------
# Fixture para client autenticado como ADMIN
# -----------------------
@pytest_asyncio.fixture
async def auth_client():
    async with AsyncClient(base_url=BASE_URL) as ac:
        # Cria o admin SE necessário (liberado só se for o primeiro user)
        await ac.post("/auth/register", json=make_admin())
        resp = await ac.post("/auth/login", json={
            "email": "admin@email.com",
            "password": "admin123"
        })
        token = resp.json()["token"]["access_token"]
        ac.headers = {"Authorization": f"Bearer {token}"}
        yield ac

# --- Teste de criação de usuário (com autenticação ADMIN) ---
@pytest.mark.asyncio
async def test_create_user_with_admin(auth_client):
    """Deve permitir admin criar novos usuários."""
    user = make_unique_user()
    response = await auth_client.post("/auth/register", json=user)
    assert response.status_code in (201, 409)
    if response.status_code == 201:
        data = response.json()
        assert data["username"] == user["username"]
        assert data["email"] == user["email"]
    else:
        assert "E-mail já cadastrado." in response.text

# --- Teste de login e refresh token ---
@pytest.mark.asyncio
async def test_refresh_token(auth_client):
    user = make_unique_user()
    # Cria novo usuário pelo admin
    resp = await auth_client.post("/auth/register", json=user)
    assert resp.status_code in (201, 409)
    # Login como user recém-criado
    login_resp = await auth_client.post("/auth/login", json={
        "email": user["email"],
        "password": user["password"]
    })
    assert login_resp.status_code == 200, login_resp.text
    tokens = login_resp.json()["token"]
    refresh_token = tokens["refresh_token"]

    refresh_response = await auth_client.post("/auth/refresh-token", json={
        "refresh_token": refresh_token
    })
    assert refresh_response.status_code == 200
    assert "access_token" in refresh_response.json()

# --- Teste de login inválido ---
@pytest.mark.asyncio
async def test_login_invalid(auth_client):
    response = await auth_client.post("/auth/login", json={
        "email": "naoexiste@email.com",
        "password": "errada"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas."

# --- Teste de refresh token inválido ---
@pytest.mark.asyncio
async def test_refresh_token_invalid(auth_client):
    response = await auth_client.post("/auth/refresh-token", json={
        "refresh_token": "token_invalido"
    })
    assert response.status_code == 401
    assert "Token de refresh inválido" in response.json()["detail"]

# --- Teste de registro sem email (validação Pydantic) ---
@pytest.mark.asyncio
async def test_create_user_missing_email(auth_client):
    response = await auth_client.post("/auth/register", json={
        "username": "joaosememail",
        "password": "senha123"
    })
    assert response.status_code == 422  # Falha de validação FastAPI

# --- Teste de login com campo ausente ---
@pytest.mark.asyncio
async def test_login_missing_password(auth_client):
    response = await auth_client.post("/auth/login", json={
        "email": "joao@gmail.com"
    })
    assert response.status_code == 422

# --- Teste para garantir não retorna senha ---
@pytest.mark.asyncio
async def test_user_response_no_password(auth_client):
    user = make_unique_user()
    await auth_client.post("/auth/register", json=user)
    login_response = await auth_client.post("/auth/login", json={
        "email": user["email"],
        "password": user["password"]
    })
    data = login_response.json()["user"]
    assert "hashed_password" not in data
    assert "password" not in data

# --- Teste de access_token válido ---
@pytest.mark.asyncio
async def test_authenticated_access(auth_client):
    user = make_unique_user()
    await auth_client.post("/auth/register", json=user)
    login_response = await auth_client.post("/auth/login", json={
        "email": user["email"],
        "password": user["password"]
    })
    access_token = login_response.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    # Exemplo: acessa rota protegida (ajuste conforme necessário)
    response = await auth_client.get("/clients/", headers=headers)
    assert response.status_code in (200, 404)
