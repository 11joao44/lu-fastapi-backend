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
from app.utils.not_found import not_found

class OrderProductsService:
    def __init__(self,
        order_repo: OrderRepository,
        product_repo: ProductRepository,
        order_products_repo: OrderProductsRepository,
    ):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.order_products_repo = order_products_repo

    async def get_by_id(self, id: int) -> OrderProductsDetailsSchema:
        data = await self.order_products_repo.get_by_id(id)
        not_found(data, OrderProductsModel, id)
        return data

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
        not_found(data, OrderProductsModel)
        return data

    async def create(self, data: OrderProductsSchema) -> OrderProductsSchema:

        if await self.order_products_repo.get_by_order_and_product(data.order_id, data.product_id):
            raise HTTPException(status.HTTP_409_CONFLICT, f"Já existe um item para order_id={data.order_id} e product_id={data.product_id}.")
        
        not_found(await self.order_repo.get_by_id(data.order_id), OrderModel, data.order_id)
        not_found(await self.order_repo.get_by_id(data.product_id), ProductModel, data.product_id)
        
        order_product = OrderProductsModel(
            order_id = data.order_id,
            product_id = data.product_id,
            quantity = data.quantity,
            price_at_moment = data.price_at_moment
        )

        return await self.order_products_repo.create(order_product)
    
    async def update(self, id: int, data: OrderProductsUpdateSchema) -> OrderProductsSchema:
        base_data = await self.order_products_repo.get_by_id(id)
        not_found(base_data, OrderProductsModel, id)
        return await self.order_products_repo.update(base_data, data)
        
    async def delete(self, id: int) -> None:
        data = await self.product_repo.get_by_id(id)
        not_found(data, OrderProductsModel, id)
        await self.order_products_repo.delete(data)
        
        