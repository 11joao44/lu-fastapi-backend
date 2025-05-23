from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

class UserRegister(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime
    updated_at: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "bearer"

class LoginResponse(BaseModel):
    token: TokenResponse
    user: UserOut

class TokenRefreshRequest(BaseModel):
    refresh_token: str
