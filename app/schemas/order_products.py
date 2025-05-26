from pydantic import BaseModel, ConfigDict, PositiveInt
from datetime import datetime
from decimal import Decimal
from typing import Optional

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
    quantity: Optional[PositiveInt]
    price_at_moment: Optional[Decimal] = None

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )