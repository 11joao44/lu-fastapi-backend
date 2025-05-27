from pydantic import EmailStr
from app.models.users import UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserModel)
    
    async def get_by_email(self, email: EmailStr) -> UserModel | None:
        return await self.get_by_field("email", email)
    