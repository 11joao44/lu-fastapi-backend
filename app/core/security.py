from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
from app.models.users import UserModel
from app.repositories.users import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import session_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(session_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Não autenticado.", 
        headers={"WWW-Authenticate": "Bearer"}
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        user_id: str = payload.get("sub")

        if user_id is None:
            raise credentials_exception
        
        user_id = int(user_id)
    except JWTError:
        raise credentials_exception

    user_repo = UserRepository(db)
    user = await user_repo.get_by_id(user_id)
    
    if user is None:
        raise credentials_exception
    
    return user

def require_admin(user: UserModel = Depends(get_current_user)):
    if not user.is_admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Ação restrita a administradores.")
    return user
