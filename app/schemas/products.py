from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime

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
