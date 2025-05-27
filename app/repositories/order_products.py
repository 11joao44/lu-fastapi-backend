from app.schemas.order_products import OrderProductsDetailsSchema
from app.models.order_products import OrderProductsModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import BaseRepository
from sqlalchemy import select
from datetime import datetime
from typing import Optional

class OrderProductsRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, OrderProductsModel)
    
    async def get_by_order_and_product(self, order_id: int, product_id: int):
        result = await self.session.execute(
            select(OrderProductsModel)
            .where(OrderProductsModel.order_id == order_id)
            .where(OrderProductsModel.product_id == product_id)
        )
        return result.scalar_one_or_none()
    
    async def list(self,
        order_id: Optional[int] = None,
        product_id: Optional[int] = None,
        quantity: Optional[int] = None,
        price_at_moment_min: Optional[int] = None,
        price_at_moment_max: Optional[int] = None,
        date_start: Optional[datetime] = None, 
        date_end: Optional[datetime] = None,
    ) -> list[OrderProductsDetailsSchema]:
        query = select(OrderProductsModel)
    
        if order_id:
            query = query.where(OrderProductsModel.order_id == order_id)
        if product_id:
            query = query.where(OrderProductsModel.product_id == product_id)
        if quantity:
            query = query.where(OrderProductsModel.quantity == quantity)
        if price_at_moment_min:
            query = query.where(OrderProductsModel.price_at_moment >= price_at_moment_min)
        if price_at_moment_max:
            query = query.where(OrderProductsModel.price_at_moment <= price_at_moment_max)
        if date_start is not None:
            query = query.where(OrderProductsModel.created_at >= date_start)
        if date_end is not None:
            query = query.where(OrderProductsModel.created_at <= date_end)
    
        result = await self.session.execute(query)
        return result.scalars().all()
