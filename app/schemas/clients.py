from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class CreateClientSchema(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str]
    cpf_cnpj: str
    address: Optional[str]
class ClientSchema(CreateClientSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    