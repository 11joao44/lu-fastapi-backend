from app.models.order_products import OrderProductsModel
from app.schemas.orders import OrderDetailsSchema
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.products import ProductModel
from app.repositories import BaseRepository
from app.models.orders import OrderModel
from sqlalchemy import select
from datetime import datetime
from typing import Optional

class OrderRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrderModel)
    
    async def list(self, 
        date_start: Optional[datetime] = None, 
        date_end: Optional[datetime] = None,
        product_id: Optional[int] = None,
        client_id: Optional[int] = None,
        section: Optional[str] = None,
        status: Optional[str] = None, 
    ) -> list[OrderDetailsSchema]:
        query = select(OrderModel)
    
        if product_id or section:
            query = query.join(OrderModel.order_products).join(OrderProductsModel.product)
    
        if client_id:
            query = query.where(OrderModel.client_id == client_id)
        if date_start is not None:
            query = query.where(OrderModel.created_at >= date_start)
        if date_end is not None:
            query = query.where(OrderModel.created_at <= date_end)
        if status is not None:
            query = query.where(OrderModel.status == status)
        if product_id:
            query = query.where(OrderProductsModel.product_id == product_id)
        if section:
            query = query.where(ProductModel.section == section)
    
        result = await self.session.execute(query)
        return result.scalars().all()
