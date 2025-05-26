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