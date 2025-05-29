from tests.conftest import get_token
from typing import Dict
import pytest


@pytest.mark.asyncio
async def register(client, db_session, body: Dict, expect_status: int):
    headers = await get_token(client, db_session, False)
    response = client.post("/clients/", json=body, headers=headers)
    assert response.status_code == expect_status, response.text
    return response

@pytest.mark.asyncio
async def test_create_client(client, db_session):
    body = {
        "name": "Cliente Tester",
        "email": "cliente@email.com",
        "phone": "4732515000",
        "cpf_cnpj": "20177173000197",
        "address": "Rua Gonçalo de Carvalho - Porto Alegre, Rio Grande do Sul"
    }
    response = await register(client, db_session, body, 201)
    data = response.json()
    assert data["name"] == "Cliente Tester"
    assert data["email"] == "cliente@email.com"
    assert data["phone"] == "4732515000"
    assert data["cpf_cnpj"] == "20177173000197"
    assert data["address"] == "Rua Gonçalo de Carvalho - Porto Alegre, Rio Grande do Sul"
    response = await register(client, db_session, body, 403)

@pytest.mark.asyncio
async def test_list_clients(client, db_session):
    headers = await get_token(client, db_session, False)
    response = client.get("/clients/", headers=headers)
    assert response.status_code == 200, response.text

# @pytest.mark.asyncio
# async def test_get_client_by_id(auth_client):
#     client_data = make_unique_client()
#     create_resp = await auth_client.post("/clients/", json=client_data)
#     assert create_resp.status_code == 201, create_resp.text
#     client_id = create_resp.json()["id"]
#     # Busca por ID
#     response = await auth_client.get(f"/clients/{client_id}")
#     assert response.status_code == 200
#     data = response.json()
#     assert data["id"] == client_id
#     assert data["name"] == client_data["name"]

# @pytest.mark.asyncio
# async def test_update_client(auth_client):
#     client_data = make_unique_client()
#     create_resp = await auth_client.post("/clients/", json=client_data)
#     assert create_resp.status_code == 201, create_resp.text
#     client_id = create_resp.json()["id"]
#     updated_data = dict(client_data)
#     updated_data["name"] = "Novo Nome"
#     response = await auth_client.patch(f"/clients/{client_id}", json=updated_data)
#     assert response.status_code == 200
#     data = response.json()
#     assert data["name"] == "Novo Nome"

# @pytest.mark.asyncio
# async def test_delete_client(auth_client):
#     client_data = make_unique_client()
#     create_resp = await auth_client.post("/clients/", json=client_data)
#     assert create_resp.status_code == 201, create_resp.text
#     client_id = create_resp.json()["id"]
#     # Deleta
#     response = await auth_client.delete(f"/clients/{client_id}")
#     assert response.status_code == 204
#     # Verifica se realmente foi deletado
#     get_resp = await auth_client.get(f"/clients/{client_id}")
#     assert get_resp.status_code == 404

# @pytest.mark.asyncio
# async def test_create_duplicate_client(auth_client):
#     client_data = make_unique_client()
#     resp1 = await auth_client.post("/clients/", json=client_data)
#     assert resp1.status_code == 201, resp1.text
#     # Segundo cadastro com o mesmo email/phone/cpf_cnpj
#     resp2 = await auth_client.post("/clients/", json=client_data)
#     assert resp2.status_code == 409
#     assert "já cadastrado" in resp2.text
