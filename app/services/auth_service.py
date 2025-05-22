from passlib.context import CryptContext
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.schemas.user import UserLogin, UserOut, UserRegister
from app.core.config import settings
from pydantic import EmailStr
from jose import JWTError, jwt
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
            hashed_password = self.hash_password(data.password)
        )
        
        return await self.user_repo.create(user)
    
    async def login_user(self, data: UserLogin):
        user = await self.user_repo.get_by_email(data.email)
        if not user or not pwd_context.verify(data.password, user.hashed_password):
            return None
        return UserOut(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_admin=user.is_admin,
            created_in=user.created_in,
            updated_in=user.updated_in
        )

    async def refresh_token(self, refresh_token: str) -> str | None:
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, settings.ALGORITHM)
            user_id = payload.get("sub")
            
            if not user_id:
                return None
            
            access_token = self.create_access_token({"sub": user_id})
            return access_token
        except JWTError:
            return None
        
    def create_access_token(self, data: dict, expire_delta: int = 30):
        to_enconde = data.copy()
        to_enconde.update({"exp": datetime.now() + timedelta(minutes=expire_delta)})
        
        return jwt.encode(to_enconde, settings.SECRET_KEY, settings.ALGORITHM)
