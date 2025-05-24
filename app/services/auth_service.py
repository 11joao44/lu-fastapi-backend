from fastapi import HTTPException
from passlib.context import CryptContext
from app.repositories.user_repository import UserRepository
from app.models.users import UserModel
from app.schemas.user import UserLogin, UserOut, UserRegister
from app.core.config import settings
from jose import JWTError, jwt
from http import HTTPStatus
from datetime import datetime, timedelta, timezone

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
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="E-mail já cadastrado.")
        
        user = UserModel(
            username = data.username,
            email = data.email,
            hashed_password = self.hash_password(data.password)
        )
        
        return await self.user_repo.create(user)
    
    async def login_user(self, data: UserLogin):
        user = await self.user_repo.get_by_email(data.email)

        if not user or not pwd_context.verify(data.password, user.hashed_password):
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Credenciais inválidas.")
            
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
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Token de refresh inválido ou expirado.")

            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Token de refresh inválido ou expirado.")

            token = self.create_access_token({"sub": user_id})
            return token

        except JWTError as e:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Token de refresh inválido ou expirado." )
        
    def create_access_token(self, data: dict, expire_delta: int = 30):
        to_encode = data.copy()
        if "sub" in to_encode:
            to_encode["sub"] = str(to_encode["sub"])
        to_encode.update({"exp": datetime.now(timezone.utc) + timedelta(minutes=expire_delta)})
        return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)

    def create_refresh_token(self, data: dict, expire_delta: int = 7 * 24 * 60):
        to_encode = data.copy()
        
        if "sub" in to_encode:
            to_encode["sub"] = str(to_encode["sub"])
        
        to_encode.update({
            "exp": datetime.now(timezone.utc) + timedelta(minutes=expire_delta),
            "type": "refresh"
        })
        return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


