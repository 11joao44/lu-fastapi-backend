from pydantic import BaseModel, ConfigDict, HttpUrl, conint
from typing import Optional
from decimal import Decimal
from datetime import date, datetime

class ProductSchema(BaseModel):
    name: str
    description: Optional[str]
    # Validações extras
    from pydantic import field_validator

    @field_validator('name')
    @classmethod
    def name_max_length(cls, v):
        if v and len(v) > 100:
            raise ValueError('O nome deve ter no máximo 100 caracteres.')
        return v

    @field_validator('description')
    @classmethod
    def description_max_length(cls, v):
        if v and len(v) > 255:
            raise ValueError('A descrição deve ter no máximo 255 caracteres.')
        return v
    price: Decimal
    barcode: Optional[str]
    section: Optional[str]
    stock: int
    expiration_date: Optional[datetime]
    image_url: Optional[str]

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

class ProductDetailsSchema(ProductSchema):
    id: int
    created_at: datetime
    updated_at: datetime

class ProductUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

    from pydantic import field_validator

    @field_validator('name')
    @classmethod
    def name_max_length(cls, v):
        if v and len(v) > 100:
            raise ValueError('O nome deve ter no máximo 100 caracteres.')
        return v

    @field_validator('description')
    @classmethod
    def description_max_length(cls, v):
        if v and len(v) > 255:
            raise ValueError('A descrição deve ter no máximo 255 caracteres.')
        return v
    price: Optional[Decimal] = None
    barcode: Optional[str] = None
    section: Optional[str] = None
    stock: Optional[int] = None
    expiration_date: Optional[date] = None
    image_url: Optional[HttpUrl] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )
