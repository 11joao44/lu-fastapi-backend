from .conftest import create_item_in_db, get_token
from decimal import Decimal
import random
import pytest


async def create_product_mock(db_session):
    from app.models.products import ProductModel
    await create_item_in_db(db_session, ProductModel, {
        "name": "Playstation 5",
        "description": f"Video Game produzido pela Sony",
        "price": float(Decimal("6199.99")),
        "barcode": 64546987879654,
        "section": "brinquedos",
        "stock": 100,
        "expiration_date": None,
        "image_url": None
    })


@pytest.mark.asyncio
async def test_create_product(db_session, client):
    headers = await get_token(client, db_session)
    body = {
        "name": "Playstation 5",
        "description": f"Video Game produzido pela Sony",
        "price": float(Decimal("6199.99")),
        "barcode": "64546987879654",
        "section": "brinquedos",
        "stock": 100,
        "expiration_date": None,
        "image_url": None
    }


    response = client.post("/products/", json=body, headers=headers)
    assert response.status_code == 201, response.text

@pytest.mark.asyncio
async def test_list_products(db_session, client):
    await create_product_mock(db_session)
    headers = await get_token(client, db_session)
    response =  client.get("/products/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Teste para garantir que não é possível criar produto com preço negativo
@pytest.mark.asyncio
async def test_create_product_with_negative_price(db_session, client):
    headers = await get_token(client, db_session)
    body = {
        "name": "Produto Inválido",
        "description": "Teste de preço negativo",
        "price": -10.00,
        "barcode": "9999999999999",
        "section": "testes",
        "stock": 10,
        "expiration_date": None,
        "image_url": None
    }
    response = client.post("/products/", json=body, headers=headers)
    assert response.status_code == 422 or response.status_code == 400
    # Opcional: checar mensagem de erro
    # assert "price" in response.text or "negativo" in response.text

# @pytest.mark.asyncio
# async def test_update_product(auth_admin_client):

# Teste: listagem de produtos filtrando por seção, preço mínimo/máximo e disponibilidade
@pytest.mark.asyncio
async def test_list_products_with_filters(db_session, client):
    headers = await get_token(client, db_session)
    # Cria produtos variados
    produtos = [
        {"name": "Produto A", "description": "A", "price": 10, "barcode": str(random.randint(1000000000000, 1999999999999)), "section": "brinquedos", "stock": 5, "expiration_date": None, "image_url": None},
        {"name": "Produto B", "description": "B", "price": 50, "barcode": str(random.randint(2000000000000, 2999999999999)), "section": "eletronicos", "stock": 0, "expiration_date": None, "image_url": None},
        {"name": "Produto C", "description": "C", "price": 100, "barcode": str(random.randint(3000000000000, 3999999999999)), "section": "brinquedos", "stock": 10, "expiration_date": None, "image_url": None},
    ]
    for prod in produtos:
        resp = client.post("/products/", json=prod, headers=headers)
        assert resp.status_code == 201

    # Filtro por seção
    resp_secao = client.get("/products/?section=brinquedos", headers=headers)
    assert resp_secao.status_code == 200
    data_secao = resp_secao.json()
    assert all(p["section"] == "brinquedos" for p in data_secao)

    # Filtro por preço mínimo
    resp_min = client.get("/products/?price_min=50", headers=headers)
    assert resp_min.status_code == 200
    data_min = resp_min.json()
    assert all(float(p["price"]) >= 50 for p in data_min)

    # Filtro por preço máximo
    resp_max = client.get("/products/?price_max=50", headers=headers)
    assert resp_max.status_code == 200
    data_max = resp_max.json()
    assert all(float(p["price"]) <= 50 for p in data_max)

    # Filtro por disponibilidade (estoque > 0)
    resp_disp = client.get("/products/?availability=true", headers=headers)
    assert resp_disp.status_code == 200
    data_disp = resp_disp.json()
    assert all(p["stock"] > 0 for p in data_disp)


# Teste: não deve permitir atualizar produto com preço negativo
@pytest.mark.asyncio
async def test_update_product_with_negative_price(db_session, client):
    headers = await get_token(client, db_session)
    # Cria produto válido
    body = {
        "name": "Produto para Atualizar",
        "description": "Teste update",
        "price": 100.00,
        "barcode": "8888888888888",
        "section": "testes",
        "stock": 10,
        "expiration_date": None,
        "image_url": None
    }
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 201
    product_id = resp.json()["id"]
    # Tenta atualizar com preço negativo
    update = {"price": -50.00}
    resp_update = client.patch(f"/products/{product_id}", json=update, headers=headers)
    assert resp_update.status_code == 422 or resp_update.status_code == 400

# Teste: não deve permitir criar produto com barcode duplicado
@pytest.mark.asyncio
async def test_create_product_with_duplicate_barcode(db_session, client):
    headers = await get_token(client, db_session)
    body = {
        "name": "Produto 1",
        "description": "Teste duplicado",
        "price": 50.00,
        "barcode": "7777777777777",
        "section": "testes",
        "stock": 5,
        "expiration_date": None,
        "image_url": None
    }
    resp1 = client.post("/products/", json=body, headers=headers)
    assert resp1.status_code == 201
    # Tenta criar outro produto com o mesmo barcode
    body2 = dict(body)
    body2["name"] = "Produto 2"
    resp2 = client.post("/products/", json=body2, headers=headers)
    assert resp2.status_code == 409

# Teste: deletar produto existente
@pytest.mark.asyncio
async def test_delete_product(db_session, client):
    headers = await get_token(client, db_session)
    body = {
        "name": "Produto para Deletar",
        "description": "Teste delete",
        "price": 30.00,
        "barcode": "6666666666666",
        "section": "testes",
        "stock": 2,
        "expiration_date": None,
        "image_url": None
    }
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 201
    product_id = resp.json()["id"]
    resp_del = client.delete(f"/products/{product_id}", headers=headers)
    assert resp_del.status_code == 204
    # Tenta deletar novamente
    resp_del2 = client.delete(f"/products/{product_id}", headers=headers)
    assert resp_del2.status_code == 404


# Teste: criação de produto sem campos obrigatórios
@pytest.mark.asyncio
async def test_create_product_missing_required_fields(db_session, client):
    headers = await get_token(client, db_session)
    # Sem nome
    body = {
        "description": "Sem nome",
        "price": 10.0,
        "barcode": "1234567890123",
        "section": "testes",
        "stock": 1
    }
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 422 or resp.status_code == 400
    # Sem preço
    body = {
        "name": "Sem Preço",
        "description": "Sem preço",
        "barcode": "1234567890124",
        "section": "testes",
        "stock": 1
    }
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 422 or resp.status_code == 400

# Teste: atualização parcial de apenas um campo
@pytest.mark.asyncio
async def test_partial_update_product(db_session, client):
    headers = await get_token(client, db_session)
    body = {
        "name": "Produto Parcial",
        "description": "Teste parcial",
        "price": 20.0,
        "barcode": "1234567890999",
        "section": "testes",
        "stock": 2,
        "expiration_date": None,
        "image_url": None
    }
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 201
    product_id = resp.json()["id"]
    update = {"name": "Nome Atualizado"}
    resp_patch = client.patch(f"/products/{product_id}", json=update, headers=headers)
    assert resp_patch.status_code == 200
    assert resp_patch.json()["name"] == "Nome Atualizado"

# Teste: criação com tipo de dado inválido
@pytest.mark.asyncio
async def test_create_product_invalid_type(db_session, client):
    headers = await get_token(client, db_session)
    body = {
        "name": "Produto Inválido",
        "description": "Tipo inválido",
        "price": "dez reais",
        "barcode": "1234567890125",
        "section": "testes",
        "stock": 1
    }
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 422 or resp.status_code == 400

# Teste: nome muito longo
@pytest.mark.asyncio
async def test_create_product_name_too_long(db_session, client):
    headers = await get_token(client, db_session)
    long_name = "A" * 300
    body = {
        "name": long_name,
        "description": "Nome longo",
        "price": 10.0,
        "barcode": "1234567890126",
        "section": "testes",
        "stock": 1
    }
    resp = client.post("/products/", json=body, headers=headers)
    assert resp.status_code == 422 or resp.status_code == 400

# Teste: busca por produto inexistente
@pytest.mark.asyncio
async def test_get_nonexistent_product(db_session, client):
    headers = await get_token(client, db_session)
    resp = client.get("/products/999999", headers=headers)
    assert resp.status_code == 404

# Teste: paginação na listagem
@pytest.mark.asyncio
async def test_list_products_pagination(db_session, client):
    headers = await get_token(client, db_session)
    # Cria 5 produtos
    for i in range(5):
        body = {
            "name": f"Produto Paginado {i}",
            "description": "Paginação",
            "price": 10.0 + i,
            "barcode": f"12345678901{i+30}",
            "section": "paginacao",
            "stock": 1,
            "expiration_date": None,
            "image_url": None
        }
        resp = client.post("/products/", json=body, headers=headers)
        assert resp.status_code == 201
    # Busca com limit=2 e offset=1
    resp = client.get("/products/?limit=2&offset=1&section=paginacao", headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2