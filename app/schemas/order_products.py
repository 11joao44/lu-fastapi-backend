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
    order_id: Optional[int] = None
    product_id: Optional[int] = None
    quantity: Optional[int] = None
    price_at_moment: Optional[Decimal] = None
    class Config:
        extra = "forbid"
        orm_mode = True