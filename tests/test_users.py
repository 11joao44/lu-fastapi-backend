import pytest
import pytest_asyncio
from httpx import AsyncClient

# --- Fixture do client HTTP ---
@pytest_asyncio.fixture
async def client():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        yield ac

# --- Teste de criação de usuário ---
@pytest.mark.asyncio
async def test_create_user(client):
    response = await client.post("/auth/register", json={
        "username": "joao",
        "email": "joao@gmail.com",
        "password": "senha123"
    })
    assert response.status_code in (201, 409)  # Usuário pode já existir

    if response.status_code == 201:
        data = response.json()
        assert data["username"] == "joao"
        assert data["email"] == "joao@gmail.com"
    else:
        # Mensagem do service ao tentar criar duplicado
        assert response.json()["detail"] == "E-mail já cadastrado."

# --- Teste de fluxo completo de refresh token ---
@pytest.mark.asyncio
async def test_refresh_token(client):
    # Garante usuário
    await client.post("/auth/register", json={
        "username": "joao",
        "email": "joao@gmail.com",
        "password": "senha123"
    })

    # Login para pegar tokens
    login_response = await client.post("/auth/login", json={
        "email": "joao@gmail.com",
        "password": "senha123"
    })
    assert login_response.status_code == 200
    tokens = login_response.json()["token"]
    refresh_token = tokens["refresh_token"]

    refresh_response = await client.post("/auth/refresh-token", json={
        "refresh_token": refresh_token
    })

    assert refresh_response.status_code == 200

    assert refresh_response.status_code == 200
    data = refresh_response.json()
    assert "access_token" in data

# --- Exemplo de teste para login inválido  ---
@pytest.mark.asyncio
async def test_login_invalid(client):
    response = await client.post("/auth/login", json={
        "email": "naoexiste@email.com",
        "password": "errada"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas."

# --- Teste de refresh token inválido ---
@pytest.mark.asyncio
async def test_refresh_token_invalid(client):
    response = await client.post("/auth/refresh-token", json={
        "refresh_token": "token_invalido"
    })
    assert response.status_code == 401
    assert "Token de refresh inválido" in response.json()["detail"]

# --- Teste de registro sem email ---
@pytest.mark.asyncio
async def test_create_user_missing_email(client):
    response = await client.post("/auth/register", json={
        "username": "joaosememail",
        "password": "senha123"
    })
    assert response.status_code == 422  # Falha de validação do FastAPI/Pydantic

# --- Teste login com campo ausente ---
@pytest.mark.asyncio
async def test_login_missing_password(client):
    response = await client.post("/auth/login", json={
        "email": "joao@gmail.com"
    })
    assert response.status_code == 422

# --- Teste para garantir não retorna senha --
@pytest.mark.asyncio
async def test_user_response_no_password(client):
    # Certifique-se de criar o usuário antes
    await client.post("/auth/register", json={
        "username": "joao",
        "email": "joao@gmail.com",
        "password": "senha123"
    })
    login_response = await client.post("/auth/login", json={
        "email": "joao@gmail.com",
        "password": "senha123"
    })
    data = login_response.json()["user"]
    assert "hashed_password" not in data
    assert "password" not in data

# --- Teste de access_token válido ---
@pytest.mark.asyncio
async def test_authenticated_access(client):
    await client.post("/auth/register", json={
        "username": "joao",
        "email": "joao@gmail.com",
        "password": "senha123"
    })
    login_response = await client.post("/auth/login", json={
        "email": "joao@gmail.com",
        "password": "senha123"
    })
    access_token = login_response.json()["token"]["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    # Exemplo: acessa rota protegida (ajuste a rota conforme sua API)
    response = await client.get("/clients/", headers=headers)
    # Pode ser 200 ou 404 se não houver clientes, mas não deve ser 401
    assert response.status_code in (200, 404)
