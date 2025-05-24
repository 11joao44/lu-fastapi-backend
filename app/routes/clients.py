from pydantic import EmailStr
from app.schemas.clients import CreateClientSchema, ClientSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.clients import ClientService
from app.repositories.clients import ClientRepository
from app.core.database import session_db
from fastapi import APIRouter, Depends
from http import HTTPStatus

router = APIRouter(tags=["clients"])

@router.get("/clients", status_code=HTTPStatus.OK)
async def list_clients(name: str | None = None, email: EmailStr | None = None, limit: int = 10, offset: int = 0, db: AsyncSession = Depends(session_db)):
    client_service = ClientService(ClientRepository(db))
    return await client_service.list_clients_service(name, email, limit, offset)

@router.get("/clients/{id}", status_code=HTTPStatus.OK, response_model=ClientSchema)
async def list_client(id: int, db: AsyncSession = Depends(session_db)): 
    client_service = ClientService(ClientRepository(db))
    return await client_service.list_client_service(id)
 
@router.post("/clients", status_code=HTTPStatus.CREATED, response_model=ClientSchema)
async def register_client(client: CreateClientSchema, db: AsyncSession = Depends(session_db)):
    client_service = ClientService(ClientRepository(db))
    return await client_service.register_client_service(client)

@router.put("/clients/{id}", status_code=HTTPStatus.OK)
async def update_client(id: int, client: CreateClientSchema, db: AsyncSession = Depends(session_db)):
    client_service = ClientService(ClientRepository(db))
    return await client_service.update_client_service(id, client)

@router.delete("/clients/{id}", status_code=HTTPStatus.NO_CONTENT)
async def delete_client(id: int, db: AsyncSession = Depends(session_db)) -> None:
    client_service = ClientService(ClientRepository(db))
    await client_service.delete_client_service(id)