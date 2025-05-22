from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

class UserRegister(BaseModel): # Para entrada (request)
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel): # Para saída (response)
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_in: datetime
    updated_in: datetime | None = None

    class Config:
        from_attributes = True  # Pydantic v2

