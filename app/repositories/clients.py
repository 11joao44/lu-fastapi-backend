from sqlalchemy.ext.asyncio import AsyncSession
from app.models.clients import ClientModel
from sqlalchemy.future import select
from pydantic import EmailStr
from typing import Any, List, Optional

from app.schemas.clients import CreateClientSchema
 
class ClientRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: str) -> ClientModel:
        result = await self.session.execute(
            select(ClientModel).where(ClientModel.id == id)
        )
        return result.scalar_one_or_none()

    async def get_by_field(self, field: str, value: Any):
        
        result = await self.session.execute(
            select(ClientModel).where(getattr(ClientModel, field) == value)
        )
        
        return result.scalar_one_or_none()
    
    async def list(self, name: Optional[str] = None, email: Optional[str] = None, limit: int = 10,offset: int = 0) -> List[ClientModel]:
        query = select(ClientModel)

        if name:
            query = query.where(ClientModel.name.ilike(f"%{name}%"))
        if email:
            query = query.where(ClientModel.email.ilike(f"%{email}%"))
            
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
    async def create(self, data: CreateClientSchema) -> ClientModel:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data
     
    async def update(self, base_data: ClientModel, update_data: CreateClientSchema) -> ClientModel:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(base_data, key, value)
        await self.session.commit()
        await self.session.refresh(base_data)
        return base_data
    
    async def delete(self, data: ClientModel) -> None:
        await self.session.delete(data)
        await self.session.commit()
