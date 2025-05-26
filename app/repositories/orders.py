from datetime import datetime
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.products import ProductModel
from app.models.order_products import OrderProductsModel
from app.models.orders import OrderModel
from app.schemas.orders import OrderDetailsSchema, OrderSchema, OrderUpdateSchema

class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> OrderModel:
        result = await self.session.execute(
            select(OrderModel).where(OrderModel.id == id)
        )
        return result.scalar_one_or_none()
    
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

    async def create(self, data: OrderSchema) -> OrderModel:
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data
    
    async def update(self, base_data: OrderModel, update_data: OrderUpdateSchema) -> OrderModel:
        for key, value in update_data.model_dump(exclude_unset=True).items():
            setattr(base_data, key, value)

        await self.session.commit()
        await self.session.refresh(base_data)
        return base_data

    async def delete(self, data: OrderSchema) -> None:
        await self.session.delete(data)
        await self.session.commit()