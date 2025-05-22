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
    created_in: datetime
    updated_in: datetime | None = None

    model_config = ConfigDict(from_attributes=True)

class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'