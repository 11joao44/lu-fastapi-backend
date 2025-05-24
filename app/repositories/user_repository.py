from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from sqlalchemy.future import select
from app.models.users import UserModel

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_email(self, email: EmailStr):
        query = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def create(self, user: UserModel) -> UserModel:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def update(self, user: UserModel) -> UserModel:
        self.session.commit()
        self.session.refresh(user)
        return user
    
    async def list(self, user: UserModel):
        query = select(user)
        result = await self.session.execute(query)
        return result.scalars().all()