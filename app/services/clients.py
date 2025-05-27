from app.repositories.clients import ClientRepository
from app.schemas.clients import ClientUpdateSchema, CreateClientSchema
from app.models.clients import ClientModel
from app.utils.get_by_id_or_404 import get_by_id_or_404
from app.utils.get_by_field_or_404 import get_by_field_or_404
from pydantic import EmailStr
from typing import Optional

class ClientService:
    def __init__(self, client_repo: ClientRepository):
        self.client_repo = client_repo
    
    async def create(self, data: CreateClientSchema) -> ClientModel:
        
        await get_by_field_or_404(
            list(CreateClientSchema.model_fields.keys()),
            self.client_repo.session,
            ClientModel,
            data
        )
        
        client = ClientModel(
            name = data.name,
            email = data.email,
            phone = data.phone,
            cpf_cnpj = data.cpf_cnpj,
            address =  data.address
        )
    
        return await self.client_repo.create(client)
    
    async def get_by_id(self, id: int) -> ClientModel:
        return await get_by_id_or_404(self.client_repo.session, ClientModel, id)
    
    async def list(self, name: Optional[str] = None, email: Optional[EmailStr] = None, limit: int = 10, offset: int = 0):
        return await self.client_repo.list(name, email, limit, offset)
    
    async def update(self, id: int, update_data: ClientUpdateSchema) -> ClientModel:
        data = await get_by_id_or_404(self.client_repo.session, ClientModel, id)
        return await self.client_repo.update(data, update_data)
    
    async def delete(self, id: int) -> None:
        data = await get_by_id_or_404(self.client_repo.session, ClientModel, id)
        await self.client_repo.delete(data)