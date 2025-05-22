from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserRegister, UserOut, UserLogin, TokenResponse, TokenRefreshRequest
from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import session_db
from http import HTTPStatus

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post('/register', status_code=HTTPStatus.CREATED, response_model=UserOut)
async def register(user: UserRegister, db: AsyncSession = Depends(session_db)):
    auth_service = AuthService(UserRepository(db))
    return await auth_service.register_user(user)

@router.post('/login', status_code=HTTPStatus.OK, response_model=UserOut)
async def login(user: UserLogin, db: AsyncSession = Depends(session_db)):
    auth_service = AuthService(UserRepository(db))
    result = await auth_service.login_user(user)
    if not result:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return result

@router.post('/refresh-token', status_code=HTTPStatus.OK, response_model=TokenResponse)
async def refresh_token(req: TokenRefreshRequest, db: AsyncSession = Depends(session_db)):
    auth_service = AuthService(UserRepository(db))
    token = await auth_service.refresh_token(req.refresh_token)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    return TokenResponse(access_token=token)