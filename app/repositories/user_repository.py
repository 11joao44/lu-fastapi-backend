from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from sqlalchemy.future import select
from app.models.user import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_email(self, email: EmailStr):
        query = select(User).where(User.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
    
    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def update(self, user: User) -> User:
        self.session.commit()
        self.session.refresh(user)
        return user
    
    async def list(self, user: User):
        query = select(user)
        result = await self.session.execute(query)
        return result.scalars().all()