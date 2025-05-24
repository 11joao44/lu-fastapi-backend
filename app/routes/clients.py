from app.models.users import UserModel
from app.schemas.clients import CreateClientSchema, ClientSchema
from app.repositories.clients import ClientRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.clients import ClientService
from app.core.security import get_current_user, require_admin
from app.core.database import session_db
from fastapi import APIRouter, Depends, status
from pydantic import EmailStr

router = APIRouter(prefix="/clients", tags=["clients"])

def get_service(db: AsyncSession = Depends(session_db)) -> ClientService:
    return ClientService(ClientRepository(db))

@router.get("/", status_code=status.HTTP_200_OK)
async def list_clients_route(
    name: str | None = None,
    email: EmailStr | None = None,
    limit: int = 10, offset: int = 0,
    service: ClientService = Depends(get_service),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Lista clientes filtrando por nome e e-mail, com paginação.
    """
    return await service.list_clients_service(name, email, limit, offset)


@router.get("/{client_id}", status_code=status.HTTP_200_OK, response_model=ClientSchema)
async def list_client_route(
    client_id: int,
    service: ClientService = Depends(get_service),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Retorna detalhes de um cliente pelo ID.
    """
    return await service.list_client_service(client_id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ClientSchema)
async def register_client_route(
    client_data: CreateClientSchema,
    service: ClientService = Depends(get_service),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Registra um novo cliente.
    """
    return await service.register_client_service(client_data)


@router.put("/{client_id}", status_code=status.HTTP_200_OK)
async def update_client_route(
    client_id: int,
    client_data: CreateClientSchema,
    service: ClientService = Depends(get_service),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Atualiza um cliente existente.
    """
    return await service.update_client_service(client_id, client_data)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client_route(
    client_id: int,
    service: ClientService = Depends(get_service),
    current_user: UserModel = Depends(require_admin)
) -> None:
    """
    Exclui um cliente pelo ID.
    """
    return await service.delete_client_service(client_id)