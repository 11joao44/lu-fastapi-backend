from typing import Optional
from app.repositories.clients import ClientRepository
from app.schemas.clients import CreateClientSchema
from app.models.clients import ClientModel
from fastapi import HTTPException, status
from pydantic import EmailStr

class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    async def register_client_service(self, data: CreateClientSchema):
        
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

        return await self.client_repo.register_client_repository(client)

    async def update_client_service(self, id: int, update_data: CreateClientSchema) -> ClientModel:
        client = await self.client_repo.update_client_repository(id, update_data)

        if not client:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente não encontrado!.")
        
        return client

    async def delete_client_service(self, id: int) -> None:
        client = await self.client_repo.get_by_id(id)

        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")
        
        await self.client_repo.delete_client_repository(client)
 
    async def list_client_service(self, id: int):
        client = await self.client_repo.get_by_id(id)

        if not client:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "Cliente não encontrado!")

        return client
    
    async def list_clients_service(self, name: Optional[str], email: Optional[EmailStr], limit: int, offset: int):
        clients = await self.client_repo.list_clients_repository(name, email, limit, offset)
        if not clients:
            raise HTTPException(status.HTTP_204_NO_CONTENT, "Nenhum cliente encontrado!")
        return clients
