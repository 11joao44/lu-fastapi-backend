from fastapi import APIRouter, HTTPException, Depends, Body, status
from app.models.users import UserModel
from app.schemas.users import LoginResponse, UserRegister, UserOut, UserLogin, TokenResponse, TokenRefreshRequest
from app.repositories.users import UserRepository
from app.services.users import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import session_db
from app.core.security import require_admin

router = APIRouter(prefix="/auth", tags=["users"])

def get_service(db: AsyncSession = Depends(session_db)) -> UserService:
    return UserService(UserRepository(db))


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def register_user_route(
    user_data: UserRegister,
    service: UserService = Depends(get_service)
):
    """Registra um novo usuário."""
    return await service.register_user_service(user_data)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login_user_route(
    user: UserLogin,
    service: UserService = Depends(get_service)
):
    """Realiza login e retorna os tokens."""
    return await service.login_user_service(user)


@router.post('/refresh-token', status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def refresh_token(
    req: TokenRefreshRequest,
    service: UserService = Depends(get_service)
):
    """Renova o access token usando o refresh token."""
    token = await service.refresh_token(req.refresh_token)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de refresh inválido ou expirado.")
    
    return TokenResponse(access_token=token, refresh_token=req.refresh_token)

@router.get('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserOut)
async def list_user_route(user_id: int, service: UserService = Depends(get_service), admin: UserModel = Depends(require_admin)):
    return await service.list_user_service(user_id)