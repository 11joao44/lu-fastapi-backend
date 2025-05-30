from .test_clients import create_client_mock
from .conftest import get_token
import pytest

# =========================
#        TESTES
# =========================

async def create_order(client, db_session, status: str="entregue", create_client=True):
    if create_client: await create_client_mock(db_session)
    
    headers = await get_token(client, db_session)
    body = {
        "client_id": 1,
        "user_id": 1,
        "status": status,
        "total_amount": "350.00",
    }
    response = client.post("/orders", json=body, headers=headers)
    return response


@pytest.mark.asyncio
async def test_create_order(client, db_session):
    response = await create_order(client, db_session)
    assert response.status_code == 201, response.text


@pytest.mark.asyncio
async def test_list_orders(client, db_session):
    await create_order(client, db_session)
    headers = await get_token(client, db_session, False)
    res = client.get("/orders/", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)

@pytest.mark.asyncio
async def test_get_order_by_id(client, db_session):
    await create_order(client, db_session)
    headers = await get_token(client, db_session, False)
    res = client.get(f"/orders/1", headers=headers)
    assert res.status_code == 200, res.text

@pytest.mark.asyncio
async def test_update_order(client, db_session):
    await create_order(client, db_session)
    payload = {
        "client_id": 1,
        "user_id": 1,
        "status": "pendente",
        "total_amount": "250.00"
    }
    headers = await get_token(client, db_session, False)
    # atualiza status
    updated = {**payload, "status": "entregue"}
    res = client.patch(f"/orders/1", json=updated, headers=headers)
    assert res.status_code == 200, res.text
    assert res.json()["status"] == "entregue"

@pytest.mark.asyncio
async def test_delete_order(db_session ,client):
    await create_order(client, db_session)
    headers = await get_token(client, db_session)
    response = client.delete(f"/orders/1", headers=headers)
    assert response.status_code == 204
    # Verifica se realmente foi deletado
    get_resp = client.get(f"/orders/1", headers=headers)
    assert get_resp.status_code == 404

@pytest.mark.asyncio
async def test_list_orders_filters(client, db_session):
    await create_order(client, db_session)
    await create_order(client, db_session, status="pendente", create_client=False)
    headers = await get_token(client, db_session)

    # filtra por 'entregue'
    res = client.get("/orders/", params={"status": "entregue"}, headers=headers)
    assert res.status_code == 200
    for item in res.json():
        assert item["status"] == "entregue"
