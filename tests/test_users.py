import pytest
from httpx import AsyncClient
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app

app = create_app()

@pytest.mark.asyncio
async def test_create_user():
    """
    Testa se o endpoint de criação de usuário retorna 201 e responde com o objeto esperado.
    """
    async with AsyncClient(app=app, base_url="http://test") as ac:
        payload = {
            "username": "yasmin",
            "email": "yasmin@email.com",
            "password": "senha123"
        }
        response = await ac.post("/users", json=payload)
        assert response.status_code == 201, response.text

        data = response.json()
        assert data["username"] == "yasmin"
        assert data["email"] == "yasmin@email.com"
        assert "id" in data
        assert "created_in" in data

        # Se seu modelo UserOut tem "is_active" e "is_admin"
        assert data["is_active"] is True
        assert data["is_admin"] is False
