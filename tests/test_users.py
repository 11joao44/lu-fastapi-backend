import pytest
from httpx import AsyncClient
from app import create_app

app = create_app()

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        response = await ac.post("/auth/register", json={
            "username": "joao",
            "email": "joao@gmail.com",
            "password": "senha123"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["username"] == "joao"
        assert data["email"] == "joao@gmail.com"
