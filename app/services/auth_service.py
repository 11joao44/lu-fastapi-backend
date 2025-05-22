from passlib.context import CryptContext
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserLogin, UserRegister
from app.core.config import settings
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, password: str, hash_password: str) -> bool:
        return pwd_context.verify(password, hash_password)
    
    async def register_user(self, data: UserRegister):
        
        if await self.user_repo.get_by_email(data.email):
            print("Email já existente")
            raise Exception("E-mail já cadastrado.")
        
        user = User(
            username = data.username,
            email = data.email,
            hashed_password = self.hash_password(data.hashed_password)
        )
        
        return await self.user_repo.create(user)

    async def autheticate_user(self, email: EmailStr, password: str):
        user = self.user_repo.get_by_email(email)
        password = self.verify_password(password, user.hash_password)
        
        if not user or not password:
            return None
        
        return user
    
    def create_access_token(self, data: dict, expire_delta: int = 30):
        to_enconde = data.copy()
        to_enconde.update({"exp": datetime.now() + timedelta(minutes=expire_delta)})
        
        return jwt.encode(to_enconde, settings.SECRET_KEY, settings.ALGORITHM)
    