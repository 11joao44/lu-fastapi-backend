import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient

# Função helper para garantir clientes únicos em cada teste
def make_unique_client():
    unique = uuid.uuid4().hex[:8]
    return {
        "name": f"Cliente_{unique}",
        "email": f"{unique}@email.com",
        "phone": f"{str(uuid.uuid4().int)[:11]}",
        "cpf_cnpj": str(uuid.uuid4().int)[:11],
        "address": f"Rua Teste, {unique}"
    }

@pytest_asyncio.fixture
async def auth_client():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        # Registra e loga o usuário admin (ajuste se necessário para seu sistema)
        await ac.post("/auth/register", json={
            "username": "admin",
            "email": "admin@email.com",
            "password": "admin123",
            "is_admin": True
        })
        resp = await ac.post("/auth/login", json={
            "email": "admin@email.com",
            "password": "admin123"
        })
        access_token = resp.json()["token"]["access_token"]
        ac.headers = {"Authorization": f"Bearer {access_token}"}
        yield ac

@pytest.mark.asyncio
async def test_create_client(auth_client):
    client_data = make_unique_client()
    response = await auth_client.post("/clients/", json=client_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == client_data["name"]
    assert data["email"] == client_data["email"]

@pytest.mark.asyncio
async def test_list_clients(auth_client):
    response = await auth_client.get("/clients/")
    assert response.status_code in (200, 204)
    if response.status_code == 200:
        data = response.json()
        assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_client_by_id(auth_client):
    client_data = make_unique_client()
    create_resp = await auth_client.post("/clients/", json=client_data)
    assert create_resp.status_code == 201, create_resp.text
    client_id = create_resp.json()["id"]
    # Busca por ID
    response = await auth_client.get(f"/clients/{client_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == client_id
    assert data["name"] == client_data["name"]

@pytest.mark.asyncio
async def test_update_client(auth_client):
    client_data = make_unique_client()
    create_resp = await auth_client.post("/clients/", json=client_data)
    assert create_resp.status_code == 201, create_resp.text
    client_id = create_resp.json()["id"]
    updated_data = dict(client_data)
    updated_data["name"] = "Novo Nome"
    response = await auth_client.put(f"/clients/{client_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Novo Nome"

@pytest.mark.asyncio
async def test_delete_client(auth_client):
    client_data = make_unique_client()
    create_resp = await auth_client.post("/clients/", json=client_data)
    assert create_resp.status_code == 201, create_resp.text
    client_id = create_resp.json()["id"]
    # Deleta
    response = await auth_client.delete(f"/clients/{client_id}")
    assert response.status_code == 204
    # Verifica se realmente foi deletado
    get_resp = await auth_client.get(f"/clients/{client_id}")
    assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_create_duplicate_client(auth_client):
    client_data = make_unique_client()
    resp1 = await auth_client.post("/clients/", json=client_data)
    assert resp1.status_code == 201, resp1.text
    # Segundo cadastro com o mesmo email/phone/cpf_cnpj
    resp2 = await auth_client.post("/clients/", json=client_data)
    assert resp2.status_code == 409
    assert "já cadastrado" in resp2.text
