from sqlalchemy.ext.asyncio import AsyncSession
from app.models.clients import ClientModel
from sqlalchemy.future import select
from pydantic import EmailStr
from typing import Any, Optional

from app.schemas.clients import CreateClientSchema

class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str) -> ClientModel:
        query = select(ClientModel).where(ClientModel.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_field(self, field: str, value: Any):
        
        result = await self.session.execute(
            select(ClientModel).where(getattr(ClientModel, field) == value)
        )
        
        return result.scalar_one_or_none()
    
    async def register_client_repository(self, client: ClientModel) -> ClientModel:
        self.session.add(client)
        await self.session.commit()
        await self.session.refresh(client)
        return client
     
    async def update_client_repository(self, id: int, client_data: CreateClientSchema) -> ClientModel:
        result = await self.session.execute(select(ClientModel).where(ClientModel.id == id))
        db_client = result.scalar_one_or_none()

        if not db_client:
            return None

        for key, value in client_data.model_dump(exclude_unset=True).items():
            setattr(db_client, key, value)

        await self.session.commit()
        await self.session.refresh(db_client)

        return db_client
    
    async def list_clients_repository(self, name: Optional[str], email: Optional[EmailStr], limit: int, offset: int) -> list[ClientModel]:
        query = select(ClientModel)
        if name:
            query = query.where(ClientModel.name.ilike(f"%{name}%"))
        if email:
            query = query.where(ClientModel.email.ilike(f"%{email}%"))
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        clients = result.scalars().all()
        return clients

    async def delete_client_repository(self, client_data: ClientModel) -> None:
        await self.session.delete(client_data)
        await self.session.commit()
