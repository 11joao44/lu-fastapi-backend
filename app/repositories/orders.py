from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.products import ProductModel
from app.models.order_products import OrderProductModel
from app.models.orders import OrderModel
from app.schemas.orders import OrderDetailsSchema, OrderSchema

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, order_id: int) -> OrderDetailsSchema:
        result = await self.session.execute(
            select(OrderModel).where(OrderModel.id == order_id)
        )
        return result.scalar_one_or_none()

    async def list_order_repository(self, order_id: int) -> OrderDetailsSchema:
        result = await self.session.execute(
            select(OrderModel).where(OrderModel.id == order_id)
        )
        return result.scalar_one_or_none()
    
    async def list_orders_repository(self, 
        date_start: Optional[datetime] = None, 
        date_end: Optional[datetime] = None,
        product_id: Optional[int] = None,
        client_id: Optional[int] = None,
        section: Optional[str] = None,
        status: Optional[str] = None, 
    ) -> list[OrderDetailsSchema]:
        query = select(OrderModel)

        if product_id or section:
            query = query.join(OrderModel.order_products).join(OrderProductModel.product)

        if client_id:
            query = query.where(OrderModel.client_id == client_id)
        if date_start is not None:
            query = query.where(OrderModel.created_at >= date_start)
        if date_end is not None:
            query = query.where(OrderModel.created_at <= date_end)
        if status is not None:
            query = query.where(OrderModel.status == status)
        if product_id:
            query = query.where(OrderProductModel.product_id == product_id)
        if section:
            query = query.where(ProductModel.section == section)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def register_order_repository(self, order_data: OrderSchema) -> OrderDetailsSchema:
        self.session.add(order_data)
        await self.session.commit()
        await self.session.refresh(order_data)
        return order_data
    
    async def update_order_repository(self, order_base: OrderSchema, order_data: OrderSchema) -> OrderDetailsSchema:
        for key, value in order_data.model_dump(exclude_unset=True).items():
            setattr(order_base, key, value)

        await self.session.commit()
        await self.session.refresh(order_base)
        return order_base

    async def delete_order_repository(self, order_data: OrderSchema) -> None:
        await self.session.delete(order_data)
        await self.session.commit()