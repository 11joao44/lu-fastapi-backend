from datetime import datetime
from typing import Optional

from fastapi import HTTPException, status as HTTPSatus
from app.models.orders import OrderModel
from app.repositories.clients import ClientRepository
from app.repositories.orders import OrderRepository
from app.repositories.users import UserRepository
from app.schemas.orders import OrderDetailsSchema, OrderSchema

class OrderService:
    def __init__(self, order_repo: OrderRepository, user_repo: UserRepository, client_repo: ClientRepository):
        self.client_repo = client_repo
        self.order_repo = order_repo
        self.user_repo = user_repo

    async def register_order_service(self, order_data: OrderSchema) -> OrderSchema:
                
        client_id = await self.client_repo.get_by_id(order_data.client_id)
        if not client_id:
            raise HTTPException(HTTPSatus.HTTP_404_NOT_FOUND, "Cliente para atribuir ao pedido não encontrado!.")

        user_id = await self.user_repo.get_by_id(order_data.user_id)
        if not user_id:
            raise HTTPException(HTTPSatus.HTTP_404_NOT_FOUND, "Usuário para atribuir ao pedido não encontrado!.")

        order = OrderModel(
            client_id = order_data.client_id,
            user_id = order_data.user_id,
            status = order_data.status,
            total_amount = order_data.total_amount
        )

        return await self.order_repo.register_order_repository(order)

    async def list_orders_service(self, 
        date_start: Optional[datetime] = None, 
        date_end: Optional[datetime] = None,
        product_id: Optional[int] = None,
        client_id: Optional[int] = None,
        section: Optional[str] = None,
        status: Optional[str] = None, 
        ) -> list[OrderDetailsSchema]:
        order = await self.order_repo.list_orders_repository(date_start, date_end, product_id, client_id, section, status)
        if not order:
            HTTPException(HTTPSatus.HTTP_404_NOT_FOUND,"Pedido não encontrado!.")
        return order

    async def list_order_service(self, order_id: int) -> OrderDetailsSchema:
        order = await self.order_repo.list_order_repository(order_id)
        if not order:
            raise HTTPException(HTTPSatus.HTTP_404_NOT_FOUND, f"Pedido refente ao ID: {order_id} não foi encontrado!.")
        return order

    async def update_order_service(self, order_id: int, order_data: OrderSchema) -> OrderSchema:
        order = await self.order_repo.get_by_id(order_id)

        if not order:
            raise HTTPException(HTTPSatus.HTTP_404_NOT_FOUND, f"Pedido refente ao ID: {order_id} não foi encontrado!.")
        
        return await self.order_repo.update_order_repository(order, order_data)

    async def delete_order_service(self, order_id: int) -> None:
        order = await self.order_repo.get_by_id(order_id)

        if not order:
            raise HTTPException(HTTPSatus.HTTP_404_NOT_FOUND, f"Pedido refente ao ID: {order_id} não foi encontrado!.")
        
        await self.order_repo.delete_order_repository(order)
        