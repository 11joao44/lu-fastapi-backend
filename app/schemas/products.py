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
    name: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]
    barcode: Optional[str]
    section: Optional[str]
    stock: Optional[int]
    expiration_date: Optional[date]
    image_url: Optional[HttpUrl]
    class Config:
        extra = "forbid"
        orm_mode = True