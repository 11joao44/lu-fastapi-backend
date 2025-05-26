from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from decimal import Decimal

class OrderProductsSchema(BaseModel):
    order_id: int
    product_id: int
    quantity: int
    price_at_moment: Decimal

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

class OrderProductsDetailsSchema(OrderProductsSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    
class OrderProductsUpdateSchema(BaseModel):
    order_id: Optional[int]
    product_id: Optional[int]
    quantity: Optional[int]
    price_at_moment: Optional[Decimal]
    class Config:
        extra = "forbid"
        orm_mode = True