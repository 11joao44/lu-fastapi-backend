from app.models.clients import ClientModel
from tests.conftest import get_token, create_item, create_item_in_db
import pytest

async def create_client_mock(db_session):
    await create_item_in_db(db_session, ClientModel, {
        "name": "Cliente Tester",
        "email": "cliente@email.com",
        "phone": "4732515000",
        "cpf_cnpj": "20177173000197",
        "address": "Rua Gonçalo de Carvalho - Porto Alegre, Rio Grande do Sul"
    })


@pytest.mark.asyncio
async def test_create_client(client, db_session):
    body = {
        "name": "Cliente Tester",
        "email": "cliente@email.com",
        "phone": "4732515000",
        "cpf_cnpj": "20177173000197",
        "address": "Rua Gonçalo de Carvalho - Porto Alegre, Rio Grande do Sul"
    }
    response = await create_item(client, db_session, "/clients/", body, 201)
    data = response.json()
    assert data["name"] == "Cliente Tester"
    assert data["email"] == "cliente@email.com"
    assert data["phone"] == "4732515000"
    assert data["cpf_cnpj"] == "20177173000197"
    assert data["address"] == "Rua Gonçalo de Carvalho - Porto Alegre, Rio Grande do Sul"


@pytest.mark.asyncio
async def test_create_client_duplicate_unique_fields(client, db_session):
    from app.models.clients import ClientModel

    unique_fields = ["email", "phone", "cpf_cnpj", "address"]

    base_data = {
        "name": "Cliente Tester",
        "email": "cliente@email.com",
        "phone": "4732515000",
        "cpf_cnpj": "20177173000197",
        "address": "Rua Gonçalo de Carvalho - Porto Alegre, Rio Grande do Sul"
    }
    
    client_model = ClientModel(**base_data)
    db_session.add(client_model)
    await db_session.commit()
    await db_session.refresh(client_model)

    body = base_data.copy()

    for field in unique_fields:
        await create_item(client, db_session, "/clients/", body, 409)
        body[field] = "1" + body[field]


@pytest.mark.asyncio
async def test_list_clients(client, db_session):
    await create_client_mock(db_session)
    headers = await get_token(client, db_session, False)
    response = client.get("/clients/", headers=headers)
    assert response.status_code == 200, response.text


@pytest.mark.asyncio
async def test_get_client_by_id(client, db_session):
    await create_client_mock(db_session)
    headers = await get_token(client, db_session, False)
    response = client.get(f"/clients/1", headers=headers)
    assert response.status_code == 200
    response = client.get(f"/clients/999", headers=headers)
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_client(db_session, client):
    await create_client_mock(db_session)
    headers = await get_token(client, db_session, False)
    updated_data  = {
        "name": "Cliente Tester",
        "email": "cliente@email.com",
        "phone": "4732515000",
        "cpf_cnpj": "20177173000197",
        "address": "Rua Gonçalo de Carvalho - Porto Alegre, Rio Grande do Sul"
    }
    response = client.patch(f"/clients/1", json=updated_data, headers=headers)
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_delete_client(db_session ,client):
    await create_client_mock(db_session)
    headers = await get_token(client, db_session)
    response = client.delete(f"/clients/1", headers=headers)
    assert response.status_code == 204
    # Verifica se realmente foi deletado
    get_resp = client.get(f"/clients/1", headers=headers)
    assert get_resp.status_code == 404
