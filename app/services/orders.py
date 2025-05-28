from datetime import datetime
from typing import Optional
from app.models.clients import ClientModel
from app.models.orders import OrderModel
from app.models.users import UserModel
from app.repositories.clients import ClientRepository
from app.repositories.orders import OrderRepository
from app.repositories.users import UserRepository
from app.schemas.orders import OrderSchema, OrderUpdateSchema
from app.utils.fecth_by_id_or_404 import fecth_by_id_or_404

class OrderService:
    def __init__(self, order_repo: OrderRepository, user_repo: UserRepository, client_repo: ClientRepository):
        self.client_repo = client_repo
        self.order_repo = order_repo
        self.user_repo = user_repo
    
    async def get_by_id(self, id: int) -> OrderModel:
        return await fecth_by_id_or_404(self.order_repo.session, OrderModel, id)
    
    async def list(self, 
        date_start: Optional[datetime] = None, 
        date_end: Optional[datetime] = None,
        product_id: Optional[int] = None,
        client_id: Optional[int] = None,
        section: Optional[str] = None,
        status: Optional[str] = None, 
    ) -> list[OrderModel]:
        return await self.order_repo.list(date_start, date_end, product_id, client_id, section, status)

    async def create(self, data: OrderSchema) -> OrderModel:
        await fecth_by_id_or_404(self.client_repo.session, ClientModel, data.client_id)
        await fecth_by_id_or_404(self.user_repo.session, UserModel, data.client_id)
    
        order = OrderModel(
            client_id = data.client_id,
            user_id = data.user_id,
            status = data.status,
            total_amount = data.total_amount
        )
    
        return await self.order_repo.create(order)
    
    async def update(self, id: int, update_data: OrderUpdateSchema) -> OrderModel:
        db_instance = await fecth_by_id_or_404(self.order_repo.session, OrderModel, id)
        return await self.order_repo.update(db_instance, update_data)
    
    async def delete(self, id: int) -> None:
        data = await fecth_by_id_or_404(self.order_repo.session, OrderModel, id)
        await self.order_repo.delete(data)
    