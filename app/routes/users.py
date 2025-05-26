from fastapi import APIRouter, HTTPException, Depends, status
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


@router.get('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserOut)
async def list(user_id: int, service: UserService = Depends(get_service), admin: UserModel = Depends(require_admin)):
    return await service.list(user_id)


@router.post('/register', status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create(data: UserRegister, service: UserService = Depends(get_service), admin: UserModel = Depends(require_admin)):
    return await service.create(data)


@router.put('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserOut)
async def update(user_id: int, service: UserService = Depends(get_service), admin: UserModel = Depends(require_admin)):
    return await service.update(user_id)


@router.delete('/users/{user_id}', status_code=status.HTTP_200_OK, response_model=UserOut)
async def delete(user_id: int, service: UserService = Depends(get_service), admin: UserModel = Depends(require_admin)):
    return await service.delete(user_id)


@router.post('/login', status_code=status.HTTP_200_OK, response_model=LoginResponse)
async def login(user: UserLogin, service: UserService = Depends(get_service)):
    return await service.login(user)


@router.post('/refresh-token', status_code=status.HTTP_200_OK, response_model=TokenResponse)
async def refresh_token(req: TokenRefreshRequest, service: UserService = Depends(get_service)):
    token = await service.refresh_token(req.refresh_token)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token de refresh inválido ou expirado.")
    
    return TokenResponse(access_token=token, refresh_token=req.refresh_token)
