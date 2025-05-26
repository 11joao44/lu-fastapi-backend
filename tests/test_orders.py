import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient

BASE_URL = "http://127.0.0.1:8000"

def make_unique_email() -> str:
    return f"user_{uuid.uuid4().hex[:8]}@test.com"

def make_unique_name(prefix: str = "Name") -> str:
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

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

@pytest_asyncio.fixture
async def make_user(auth_client: AsyncClient) -> int:
    """
    Cria um usuário comum e retorna o seu ID.
    """
    user_payload = {
        "username": make_unique_name("user"),
        "email": make_unique_email(),
        "password": "user123456"
    }
    res = await auth_client.post("/auth/register", json=user_payload)
    assert res.status_code == 201, f"Não registrou user: {res.text}"
    return res.json()["id"]

@pytest_asyncio.fixture
async def make_client(auth_client: AsyncClient) -> int:
    """
    Cria um cliente e retorna o seu ID.
    """
    client_payload = {
        "name": make_unique_name("client"),
        "cpf_cnpj": str(uuid.uuid4().int)[:11],
        "email": make_unique_email(),
        "phone": str(uuid.uuid4().int)[:11],
        "address": f"Rua Teste, {str(uuid.uuid4().int)[:3]}"
    }
    res = await auth_client.post("/clients/", json=client_payload)
    assert res.status_code == 201, f"Não registrou client: {res.text}"
    return res.json()["id"]

# =========================
#        TESTES
# =========================

@pytest.mark.asyncio
async def test_create_order(auth_client, make_client, make_user):
    body = {
        "client_id": make_client,
        "user_id": make_user,
        "status": "entregue",
        "total_amount": "350.00",
    }
    r = await auth_client.post("/orders/", json=body)
    assert r.status_code == 201, r.text
    js = r.json()
    assert js["client_id"] == make_client
    assert js["user_id"]   == make_user

@pytest.mark.asyncio
async def test_list_orders(auth_client):
    """Listagem de pedidos deve retornar 200 e uma lista."""
    res = await auth_client.get("/orders/")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

@pytest.mark.asyncio
async def test_get_order_by_id(auth_client, make_client, make_user):
    """GET /orders/{id} após criar, deve retornar 200 e o mesmo ID."""
    # cria
    payload = {
        "client_id": make_client,
        "user_id": make_user,
        "status": "entregue",
        "total_amount": "200.00"
    }
    create = await auth_client.post("/orders/", json=payload)
    assert create.status_code == 201
    order_id = create.json()["id"]

    # busca
    res = await auth_client.get(f"/orders/{order_id}")
    assert res.status_code == 200
    assert res.json()["id"] == order_id

@pytest.mark.asyncio
async def test_update_order(auth_client, make_client, make_user):
    """PUT /orders/{id} deve atualizar o status do pedido."""
    # cria
    payload = {
        "client_id": make_client,
        "user_id": make_user,
        "status": "pendente",
        "total_amount": "250.00"
    }
    create = await auth_client.post("/orders/", json=payload)
    assert create.status_code == 201
    order_id = create.json()["id"]

    # atualiza status
    updated = {**payload, "status": "entregue"}
    res = await auth_client.patch(f"/orders/{order_id}", json=updated)
    assert res.status_code == 200
    assert res.json()["status"] == "entregue"

@pytest.mark.asyncio
async def test_delete_order(auth_client, make_client, make_user):
    """DELETE /orders/{id} deve retornar 204 e depois 404."""
    # cria
    payload = {
        "client_id": make_client,
        "user_id": make_user,
        "status": "pendente",
        "total_amount": "300.00"
    }
    create = await auth_client.post("/orders/", json=payload)
    assert create.status_code == 201
    order_id = create.json()["id"]

    # deleta
    res = await auth_client.delete(f"/orders/{order_id}")
    assert res.status_code == 204

    # verifica inexistência
    notfound = await auth_client.get(f"/orders/{order_id}")
    assert notfound.status_code == 404

@pytest.mark.asyncio
async def test_list_orders_filters(auth_client, make_client, make_user):
    """GET /orders/?status=entregue deve filtrar pelo status."""
    # cria dois pedidos com status alternados
    for i in range(2):
        await auth_client.post("/orders/", json={
            "client_id": make_client,
            "user_id": make_user,
            "status": "entregue" if i % 2 == 0 else "pendente",
            "total_amount": str(100 + i * 10)
        })

    # filtra por 'entregue'
    res = await auth_client.get("/orders/", params={"status": "entregue"})
    assert res.status_code == 200
    for item in res.json():
        assert item["status"] == "entregue"
