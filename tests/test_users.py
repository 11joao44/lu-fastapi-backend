# tests/test_users.py

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

    # Usa o refresh token
    refresh_response = await client.post("/auth/refresh-token", json={
        "req": {"refresh_token": refresh_token}
    })
    assert refresh_response.status_code == 200
    data = refresh_response.json()
    assert "access_token" in data

# --- Exemplo de teste para login inválido (opcional) ---
@pytest.mark.asyncio
async def test_login_invalid(client):
    response = await client.post("/auth/login", json={
        "email": "naoexiste@email.com",
        "password": "errada"
    })
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciais inválidas."
