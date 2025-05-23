from fastapi import APIRouter
from http import HTTPStatus

router = APIRouter(tags=["clients"])

@router.get("/clients", status_code=HTTPStatus.OK)
def list_clients():
    return []

@router.get("/clients/{id}", status_code=HTTPStatus.OK)
def list_client(id: int):
    return []

@router.post("/clients", status_code=HTTPStatus.CREATED)
def create_client():
    return []

@router.put("/clients/{id}", status_code=HTTPStatus.OK)
def update_client(id: int):
    return {}

@router.delete("/clients/{id}", status_code=HTTPStatus.NO_CONTENT)
def delete_client(id: int):
    return None