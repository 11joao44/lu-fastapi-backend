from pydantic import BaseModel, ConfigDict, HttpUrl, conint
from typing import Optional
from decimal import Decimal
from datetime import date, datetime

class ProductSchema(BaseModel):
    name: str
    description: Optional[str]
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
    price: Optional[Decimal] = None
    barcode: Optional[str] = None
    section: Optional[str] = None
    stock: Optional[int] = None
    expiration_date: Optional[date] = None
    image_url: Optional[HttpUrl] = None
    class Config:
        extra = "forbid"
        orm_mode = True