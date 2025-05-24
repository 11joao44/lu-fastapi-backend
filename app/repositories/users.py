from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr
from sqlalchemy.future import select
from app.models.users import UserModel

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def get_by_id(self, user_id: int) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: EmailStr) -> UserModel | None:
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return result.scalar_one_or_none()
    
    async def create(self, user: UserModel) -> UserModel:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
    
    async def update(self, user: UserModel) -> UserModel:
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user: UserModel) -> None:
        await self.session.delete(user)
        await self.session.commit()
