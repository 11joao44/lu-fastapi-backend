from fastapi import APIRouter, Depends
from http import HTTPStatus
from app.schemas.user import UserSchema, UserRegister, UserOut, UserLogin
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import session_db

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/register', status_code=HTTPStatus.CREATED, response_model=UserOut)
async def register(user: UserRegister, db: AsyncSession = Depends(session_db)):
    auth_service = AuthService(UserRepository(db))
    return await auth_service.register_user(user)
