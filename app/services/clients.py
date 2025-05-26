from app.repositories.clients import ClientRepository
from app.schemas.clients import ClientUpdateSchema, CreateClientSchema
from app.models.clients import ClientModel
from app.utils.not_found import not_found
from fastapi import HTTPException, status
from pydantic import EmailStr
from typing import Optional

class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    async def get_by_id(self, id: int) -> ClientModel:
        client = await self.client_repo.get_by_id(id)
        not_found(client, ClientModel, id)
        return client

    async def list(self, name: Optional[str], email: Optional[EmailStr], limit: int, offset: int):
        clients = await self.client_repo.list(name, email, limit, offset)
        not_found(clients, ClientModel)
        return clients

    async def create(self, data: CreateClientSchema) -> ClientModel:
        
        for column in ["email", "phone", "name", "address", "cpf_cnpj"]:
            if await self.client_repo.get_by_field(column, getattr(data, column)):
                raise HTTPException(status.HTTP_409_CONFLICT, f"{column} já cadastrado.")
                
        client = ClientModel(
            name = data.name,
            email = data.email,
            phone = data.phone,
            cpf_cnpj = data.cpf_cnpj,
            address =  data.address
        )

        return await self.client_repo.create(client)

    async def update(self, id: int, data: ClientUpdateSchema) -> ClientModel:
        client = await self.client_repo.get_by_id(id)
        not_found(client, ClientModel, id)
        return await self.client_repo.update(client, data)
    
    async def delete(self, id: int) -> None:
        client = await self.client_repo.get_by_id(id)
        not_found(client, ClientModel, id)
        await self.client_repo.delete(client)
 