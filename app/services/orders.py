from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status as HTTPSatus
from app.models.orders import OrderModel
from app.repositories.clients import ClientRepository
from app.repositories.orders import OrderRepository
from app.repositories.users import UserRepository
from app.schemas.orders import OrderDetailsSchema, OrderSchema, OrderUpdateSchema
from app.utils.not_found import not_found

class OrderService:
    def __init__(self, order_repo: OrderRepository, user_repo: UserRepository, client_repo: ClientRepository):
        self.client_repo = client_repo
        self.order_repo = order_repo
        self.user_repo = user_repo


    async def get_by_id(self, id: int) -> OrderModel:
        order = await self.order_repo.get_by_id(id)
        not_found(order, OrderModel, id)
        return order


    async def list(self, 
        date_start: Optional[datetime] = None, 
        date_end: Optional[datetime] = None,
        product_id: Optional[int] = None,
        client_id: Optional[int] = None,
        section: Optional[str] = None,
        status: Optional[str] = None, 
    ) -> list[OrderModel]:
        order = await self.order_repo.list(date_start, date_end, product_id, client_id, section, status)
        not_found(order, OrderModel)
        return order


    async def create(self, data: OrderSchema) -> OrderModel:
                
        client_id = await self.client_repo.get_by_id(data.client_id)
        not_found(client_id, OrderModel, data.client_id)

        user_id = await self.user_repo.get_by_id(data.user_id)
        not_found(user_id, OrderModel, data.user_id)

        order = OrderModel(
            client_id = data.client_id,
            user_id = data.user_id,
            status = data.status,
            total_amount = data.total_amount
        )

        return await self.order_repo.create(order)


    async def update(self, id: int, data: OrderUpdateSchema) -> OrderModel:
        order = await self.order_repo.get_by_id(id)
        not_found(order, OrderModel, id)
        return await self.order_repo.update(order, data)


    async def delete(self, id: int) -> None:
        order = await self.order_repo.get_by_id(id)
        not_found(order, OrderModel, id)
        await self.order_repo.delete(order)
        