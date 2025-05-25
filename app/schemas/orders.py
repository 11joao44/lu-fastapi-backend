from typing import List
from pydantic import BaseModel, ConfigDict
from app.schemas.products import ProductSchema
from datetime import datetime
from decimal import Decimal

class OrderSchema(BaseModel):
    client_id: int
    user_id: int
    status: str
    total_amount: Decimal

    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )

class OrderDetailsSchema(OrderSchema):
    id: int
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )
    