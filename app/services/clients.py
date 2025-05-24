from app.schemas.clients import CreateClientSchema, ClientSchema
from app.repositories.clients import ClientRepository
from app.models.clients import ClientModel
from fastapi import HTTPException
from pydantic import EmailStr
from http import HTTPStatus

class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo

    async def register_client_service(self, data: CreateClientSchema):
        
        if await self.client_repo.get_by_email(data.email):
            raise HTTPException(HTTPStatus.CONFLICT,"E-mail já cadastrado.")
        
        if await self.client_repo.get_by_address(data.address):
            raise HTTPException(HTTPStatus.CONFLICT,"Endereço já cadastrado.")
        
        if await self.client_repo.get_by_cpf_cnpj(data.cpf_cnpj):
            raise HTTPException(HTTPStatus.CONFLICT,"CPF ou CNPJ já cadastrado.")
        
        if await self.client_repo.get_by_phone(data.phone):
            raise HTTPException(HTTPStatus.CONFLICT,"Telefone já cadastrado.")
            
        client = ClientModel(
            name = data.name,
            email = data.email,
            phone = data.phone,
            cpf_cnpj = data.cpf_cnpj,
            address =  data.address
        )

        return await self.client_repo.create(client)

    async def update_client_service(self, id: int, update_data: CreateClientSchema) -> ClientModel:
        client = await self.client_repo.update_client_repository(id, update_data)

        if not client:
            raise HTTPException(HTTPStatus.NO_CONTENT, "Cliente não encontrado!.")
        
        return client

    async def delete_client_service(self, id: int) -> None:
        client = await self.client_repo.get_by_id(id)
        if not client:
            raise HTTPException(status_code=HTTPStatus.NO_CONTENT, detail="Cliente não encontrado.")
        await self.client_repo.delete_client_repository(client)
 
    async def list_client_service(self, id: int):
        client = await self.client_repo.get_by_id(id)

        if not client:
            raise HTTPException(HTTPStatus.NO_CONTENT, "Cliente não encontrado!")

        return client
    
    async def list_clients_service(self, name: str | None, email: EmailStr | None, limit: int, offset: int):
        
        clients = await self.client_repo.get_client_all(name, email, limit, offset)

        if not clients:
            raise HTTPException(HTTPStatus.NO_CONTENT, "Nenhum cliente não encontrado!")

        return clients