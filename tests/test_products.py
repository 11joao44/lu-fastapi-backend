import uuid
import pytest
import pytest_asyncio
from httpx import AsyncClient
from decimal import Decimal

# Helper para produto único
def make_unique_product():
    unique = uuid.uuid4().hex[:8]
    return {
        "name": f"Produto_{unique}",
        "description": f"Descrição do produto {unique}",
        "price": float(Decimal("10.99")),
        "barcode": f"barcode{unique}",
        "section": "brinquedos",
        "stock": 100,
        "expiration_date": None,
        "image_url": None
    }

@pytest_asyncio.fixture
async def auth_admin_client():
    async with AsyncClient(base_url="http://127.0.0.1:8000") as ac:
        # Cria e loga admin
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
async def test_create_product(auth_admin_client):
    product_data = make_unique_product()
    response = await auth_admin_client.post("/products/", json=product_data)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == product_data["name"]
    assert float(data["price"]) == product_data["price"]

@pytest.mark.asyncio
async def test_list_products(auth_admin_client):
    response = await auth_admin_client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_product_by_id(auth_admin_client):
    product_data = make_unique_product()
    create_resp = await auth_admin_client.post("/products/", json=product_data)
    assert create_resp.status_code == 201, create_resp.text
    product_id = create_resp.json()["id"]
    print("id falha:", create_resp.json())
    response = await auth_admin_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == product_data["name"]

@pytest.mark.asyncio
async def test_update_product(auth_admin_client):
    product_data = make_unique_product()
    create_resp = await auth_admin_client.post("/products/", json=product_data)
    assert create_resp.status_code == 201, create_resp.text
    product_id = create_resp.json()["id"]
    print("id falha:", create_resp.json())
    updated_data = dict(product_data)
    updated_data["name"] = "Produto Atualizado"
    response = await auth_admin_client.put(f"/products/{product_id}", json=updated_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Produto Atualizado"

@pytest.mark.asyncio
async def test_delete_product(auth_admin_client):
    product_data = make_unique_product()
    create_resp = await auth_admin_client.post("/products/", json=product_data)
    assert create_resp.status_code == 201, create_resp.text
    product_id = create_resp.json()["id"]
    print("id falha:", create_resp.json())
    response = await auth_admin_client.delete(f"/products/{product_id}")
    assert response.status_code == 204
    # Verifica que deletou
    get_resp = await auth_admin_client.get(f"/products/{product_id}")
    assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_create_duplicate_product_barcode(auth_admin_client):
    product_data = make_unique_product()
    resp1 = await auth_admin_client.post("/products/", json=product_data)
    assert resp1.status_code == 201, resp1.text
    # Tenta criar novamente com mesmo barcode
    resp2 = await auth_admin_client.post("/products/", json=product_data)
    assert resp2.status_code == 409
    assert "já foi cadastrado" in resp2.text
