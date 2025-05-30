import pytest
from decimal import Decimal
from .conftest import get_token

@pytest.mark.asyncio
async def test_products_requires_authentication(client):
    resp = client.get("/products/")
    assert resp.status_code == 401
    body = {
        "name": "Produto sem auth",
        "description": "Teste",
        "price": 10.0,
        "barcode": "9999999999999",
        "section": "auth",
        "stock": 1,
        "expiration_date": None,
        "image_url": None
    }
    resp = client.post("/products/", json=body)
    assert resp.status_code == 401

@pytest.mark.asyncio
async def test_delete_requires_admin(db_session, client):
    headers = await get_token(client, db_session, is_admin=False)
    body = {
        "name": "Produto não admin",
        "description": "Teste",
        "price": 10.0,
        "barcode": "8888888888888",
        "section": "auth",
        "stock": 1,
        "expiration_date": None,
        "image_url": None
    }
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 201
    product_id = resp.json()["id"]
    resp = client.delete(f"/products/{product_id}", headers=headers)
    assert resp.status_code == 403

@pytest.mark.asyncio
async def test_product_name_description_length(db_session, client):
    headers = await get_token(client, db_session)
    body = {
        "name": "A" * 100,
        "description": "B" * 255,
        "price": 10.0,
        "barcode": "7777777777777",
        "section": "limite",
        "stock": 1,
        "expiration_date": None,
        "image_url": None
    }
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 201
    body["name"] = "A" * 101
    body["barcode"] = "7777777777778"
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 422
    body["name"] = "Nome válido"
    body["description"] = "B" * 256
    body["barcode"] = "7777777777779"
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 422

@pytest.mark.asyncio
async def test_create_update_with_optional_fields(db_session, client):
    headers = await get_token(client, db_session)
    body = {
        "name": "Produto opcional",
        "description": "Teste",
        "price": 10.0,
        "barcode": "6666666666666",
        "section": "opcional",
        "stock": 1,
        "expiration_date": None,
        "image_url": None
    }
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 201
    product_id = resp.json()["id"]
    patch = {"price": 20.0}
    resp = client.patch(f"/products/{product_id}", json=patch, headers=headers)
    assert resp.status_code == 200
    assert float(resp.json()["price"]) == 20.0

@pytest.mark.asyncio
async def test_concurrent_barcode_creation(db_session, client):
    headers = await get_token(client, db_session)
    body = {
        "name": "Concorrente 1",
        "description": "Teste",
        "price": 10.0,
        "barcode": "5555555555555",
        "section": "concorrencia",
        "stock": 1,
        "expiration_date": None,
        "image_url": None
    }
    resp1 = client.post("/products/", json=body, headers=headers)
    body["name"] = "Concorrente 2"
    resp2 = client.post("/products/", json=body, headers=headers)
    assert resp1.status_code == 201
    assert resp2.status_code in (409, 422)

@pytest.mark.asyncio
async def test_list_many_products_performance(db_session, client):
    headers = await get_token(client, db_session)
    for i in range(30):
        body = {
            "name": f"Perf {i}",
            "description": "Teste perf",
            "price": float(Decimal("10.00")),
            "barcode": f"44444444444{i:02}",
            "section": "perf",
            "stock": 1,
            "expiration_date": None,
            "image_url": None
        }
        resp = client.post("/products/", json=body, headers=headers)
        assert resp.status_code == 201
    resp = client.get("/products/?limit=50&section=perf", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 30
