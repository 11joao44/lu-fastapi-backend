from fastapi.testclient import TestClient
from app import create_app

app = create_app()
client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={
        "username": "joao",
        "email": "joao@gmail.com",
        "password": "senha123"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "joao"
    assert data["email"] == "joao@gmail.com"
    assert "id" in data
    assert "created_in" in data
    assert data["is_active"] is True
    assert data["is_admin"] is False
