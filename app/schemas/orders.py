from typing import List, Optional
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
    

class OrderUpdateSchema(BaseModel):
    client_id: Optional[int] = None
    user_id: Optional[int] = None
    status: Optional[str] = None
    total_amount: Optional[Decimal] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        extra="forbid"
    )