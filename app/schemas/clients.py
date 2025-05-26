from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional
from datetime import datetime

class CreateClientSchema(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str]
    cpf_cnpj: str
    address: Optional[str]
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

class ClientSchema(CreateClientSchema):
    id: int
    created_at: datetime
    updated_at: datetime

class ClientUpdateSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    cpf_cnpj: Optional[str] = None
    address: Optional[str] = None
    class Config:
        extra = "forbid"
        orm_mode = True