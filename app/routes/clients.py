from app.models.users import UserModel
from app.schemas.clients import ClientUpdateSchema, CreateClientSchema, ClientSchema
from app.repositories.clients import ClientRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.clients import ClientService
from app.core.security import locked_route, require_admin
from app.core.database import session_db
from fastapi import APIRouter, Depends, Query, status
from pydantic import EmailStr
from typing import Optional

router = APIRouter(prefix="/clients", tags=["clients"])

def get_service(db: AsyncSession = Depends(session_db), locked: UserModel = Depends(locked_route)) -> ClientService:
    return ClientService(ClientRepository(db))
 

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ClientSchema)
async def get_by_id(id: int, service: ClientService = Depends(get_service)):
    return await service.get_by_id(id)


@router.get("/", status_code=status.HTTP_200_OK)
async def list(
    name: Optional[str] = Query(None, description="Nome do cliente que deseja filtrar", examples={"exemplo": {"name": "Gustavo"}}),
    email: Optional[EmailStr] = Query(None, description="E-mail do cliente que deseja filtrar", examples={"exemplo": {"email": "11joao44@gmail.com"}}),
    limit: int = 10, offset: int = 0,
    service: ClientService = Depends(get_service)
):
    return await service.list(name, email, limit, offset)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ClientSchema)
async def create(data: CreateClientSchema, service: ClientService = Depends(get_service)):
    return await service.create(data)


@router.patch("/{id}", status_code=status.HTTP_200_OK)
async def update(id: int, data: ClientUpdateSchema,  service: ClientService = Depends(get_service)):
    return await service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, service: ClientService = Depends(get_service), admin: UserModel = Depends(require_admin)) -> None:
    return await service.delete(id)