from typing import Any, Dict
from fastapi import HTTPException, status
from passlib.context import CryptContext
from app.repositories.users import UserRepository
from app.models.users import UserModel
from app.schemas.users import UserLogin, UserOut, UserRegister
from app.core.config import settings
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from app.utils.get_by_id_or_404 import get_by_id_or_404

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo
        
    async def delete(self, id: int) -> None:
        data = await get_by_id_or_404(self.user_repo.session, UserModel, id)
        await self.user_repo.delete(data)
    
    async def list(self, id: int) -> UserModel:
        user = await self.user_repo.get_by_field("id", id)
        return user
    
    async def create(self, data: UserRegister) -> UserModel:
    
        if await self.user_repo.get_by_email(data.email):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="E-mail já cadastrado.")
    
        if len(data.password) < 8:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Senha deve ter pelo menos 8 caracteres.")
    
        user = UserModel(
            username = data.username,
            email = data.email,
            hashed_password = self.hash_password(data.password)
        )
    
        return await self.user_repo.create(user)
    
    async def update(self, id: int, update_data: UserRegister) -> UserModel:
        db_instance = await get_by_id_or_404(self.user_repo.session, UserModel, id)
        return await self.user_repo.update(db_instance, update_data)
    
    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def verify_password(self, password: str, hash_password: str) -> bool:
        return pwd_context.verify(password, hash_password)
    
    async def login(self, data: UserLogin) -> Dict[str, Any]:
        user = await self.user_repo.get_by_email(data.email)
    
        if not user or not pwd_context.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciais inválidas.")
    
        return {
            "token": {
                "access_token": self.create_access_token({"sub": user.id}),
                "refresh_token": self.create_refresh_token({"sub": user.id}),
                "token_type": "bearer",
            },
            "user": UserOut.model_validate(user)
        }
    
    async def refresh_token(self, refresh_token: str) -> str:
        try:
            payload = jwt.decode(refresh_token, settings.SECRET_KEY, settings.ALGORITHM)
    
            if payload.get("type") != "refresh":
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de refresh inválido ou expirado.")
    
            user_id = payload.get("sub")
    
            if not user_id:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de refresh inválido ou expirado.")
    
            if not await self.user_repo.get_by_id(int(user_id)):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não existe ou está desativado.")
    
            return self.create_access_token({"sub": user_id})
    
        except JWTError as e:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de refresh inválido ou expirado." )
        
    def create_access_token(self, data: dict, expire_delta: int = 30) -> str:
        to_encode = data.copy()
        to_encode["sub"] = str(to_encode.get("sub"))
    
        now = datetime.now(timezone.utc)
        to_encode.update({"exp": now + timedelta(minutes=expire_delta), "iat": now, "nbf": now})
    
        return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    
    def create_refresh_token(self, data: dict, expire_delta: int = 7 * 24 * 60) -> str:
        to_encode = data.copy()
        to_encode["sub"] = str(to_encode.get("sub"))
    
        now = datetime.now(timezone.utc)
        to_encode.update({"exp": now + timedelta(minutes=expire_delta), "type": "refresh", "iat": now, "nbf": now})
    
        return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


