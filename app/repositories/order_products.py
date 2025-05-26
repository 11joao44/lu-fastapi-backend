from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.order_products import OrderProductsModel
from app.schemas.order_products import OrderProductsDetailsSchema, OrderProductsSchema, OrderProductsUpdateSchema

class OrderProductsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> OrderProductsDetailsSchema:
        result = await self.session.execute(
            select(OrderProductsModel).where(OrderProductsModel.id == id)
        )
        return result.scalar_one_or_none()
    
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

    async def create(self, data: OrderProductsSchema) -> OrderProductsSchema:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data
    
    async def update(self, base_data: OrderProductsSchema, update_data: OrderProductsUpdateSchema) -> OrderProductsSchema:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(base_data, key, value)

        await self.session.commit()
        await self.session.refresh(base_data)
        return base_data

    async def delete(self, data: OrderProductsSchema) -> None:
        await self.session.delete(data)
        await self.session.commit()