from fastapi import APIRouter, HTTPException, Depends, Body
from app.schemas.user import LoginResponse, UserRegister, UserOut, UserLogin, TokenResponse, TokenRefreshRequest
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

@router.post('/login', status_code=HTTPStatus.OK, response_model=LoginResponse)
async def login(user: UserLogin, db: AsyncSession = Depends(session_db)):
    auth_service = AuthService(UserRepository(db))
    return await auth_service.login_user(user)

@router.post('/refresh-token', status_code=HTTPStatus.OK, response_model=TokenResponse)
async def refresh_token(req: TokenRefreshRequest = Body(..., embed=True), db: AsyncSession = Depends(session_db)):
    auth_service = AuthService(UserRepository(db))
    token = await auth_service.refresh_token(req.refresh_token)
    if not token:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Token de refresh inválido ou expirado.")
    return TokenResponse(access_token=token, refresh_token=req.refresh_token)
