from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import BaseRepository
from app.models.clients import ClientModel
from sqlalchemy.future import select
from typing import List, Optional

class ClientRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ClientModel)
    
    async def list(self, name: Optional[str] = None, email: Optional[str] = None, limit: int = 10,offset: int = 0) -> List[ClientModel]:
        query = select(ClientModel)
    
        if name:
            query = query.where(ClientModel.name.ilike(f"%{name}%"))
        if email:
            query = query.where(ClientModel.email.ilike(f"%{email}%"))
    
        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()
    
