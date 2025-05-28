from datetime import datetime
from typing import Optional
from fastapi import HTTPException, status
from app.models.order_products import OrderProductsModel
from app.models.orders import OrderModel
from app.models.products import ProductModel
from app.repositories.orders import OrderRepository
from app.repositories.products import ProductRepository
from app.schemas.order_products import OrderProductsDetailsSchema, OrderProductsSchema, OrderProductsUpdateSchema
from app.repositories.order_products import OrderProductsRepository
from app.utils.fecth_by_id_or_404 import fecth_by_id_or_404
from app.utils.check_unique_fields import check_unique_fields
 
class OrderProductsService:
    def __init__(self,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
        order_products_repo: OrderProductsRepository,
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.order_products_repo = order_products_repo
    
    async def list(self,     
        order_id: Optional[int] = None,
        product_id: Optional[int] = None,
        quantity: Optional[int] = None,
        price_at_moment_min: Optional[int] = None,
        price_at_moment_max: Optional[int] = None,
        date_start: Optional[datetime] = None, 
        date_end: Optional[datetime] = None
    ) -> list[OrderProductsDetailsSchema]:
        data = await self.order_products_repo.list(order_id, product_id, quantity, price_at_moment_min, price_at_moment_max, date_start, date_end)
        return data
    
    async def create(self, data: OrderProductsSchema) -> OrderProductsModel:
    
        if await self.order_products_repo.get_by_order_and_product(data.order_id, data.product_id):
            raise HTTPException(status.HTTP_409_CONFLICT, f"Já existe um item para order_id={data.order_id} e product_id={data.product_id}.")
    
        await fecth_by_id_or_404(self.order_repo.session, OrderModel, data.order_id)
        await fecth_by_id_or_404(self.product_repo.session, ProductModel,  data.product_id)
    
        order_product = OrderProductsModel(
            order_id = data.order_id,
            product_id = data.product_id,
            quantity = data.quantity,
            price_at_moment = data.price_at_moment
        )
    
        return await self.order_products_repo.create(order_product)
    
    async def get_by_id(self, id: int) -> OrderProductsDetailsSchema:
        return await fecth_by_id_or_404(self.order_products_repo.session, OrderProductsModel, id)
    
    async def update(self, id: int, update_data: OrderProductsUpdateSchema) -> OrderProductsSchema:
        db_instance = await fecth_by_id_or_404(self.order_products_repo.session, OrderProductsModel, id)
        await fecth_by_id_or_404(self.order_repo.session, OrderModel, db_instance.order_id)
        await fecth_by_id_or_404(self.product_repo.session, ProductModel,  db_instance.product_id)
        return await self.order_products_repo.update(db_instance, update_data)
    
    async def delete(self, id: int) -> None:
        data = await fecth_by_id_or_404(self.order_products_repo.session, OrderProductsModel, id)
        await self.order_products_repo.delete(data)
    