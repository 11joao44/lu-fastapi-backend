from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from decimal import Decimal

from app.models.products import ProductModel
from app.schemas.products import ProductDetailsSchema, ProductSchema


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, id: int) -> ProductDetailsSchema:
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.id == id)
        )
        return result.scalar_one_or_none()
    
    async def get_by_barcode(self, barcode: str):
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.barcode == barcode)
        )
        return result.scalar_one_or_none()
    
    async def register_product_repository(self, product_data: ProductModel) -> ProductDetailsSchema:
        self.session.add(product_data)
        await self.session.commit()
        await self.session.refresh(product_data)
        return product_data
    
    async def list_products_repository(
        self,
        limit: int,
        offset: int,
        section: Optional[str] = None,
        price_min: Optional[Decimal] = None,
        price_max: Optional[Decimal] = None,
        availability: Optional[bool] = None
    ):
        query = select(ProductModel)

        if section:
            query = query.where(ProductModel.section.ilike(f"%{section}%"))
        if price_min is not None:
            query = query.where(ProductModel.price >= price_min)
        if price_max is not None:
            query = query.where(ProductModel.price <= price_max)
        if availability is not None:
            if availability:
                query = query.where(ProductModel.stock > 0)
            else:
                query = query.where(ProductModel.stock <= 0)

        query = query.offset(offset).limit(limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def update_product_repository(self, client_base: ProductSchema, client_data: ProductSchema) -> ProductDetailsSchema:
        for key, value in client_data.model_dump(exclude_unset=True).items():
            setattr(client_base, key, value)

        await self.session.commit()
        await self.session.refresh(client_base)

        return client_base
    
    async def delete_product_repository(self,  product_data: ProductModel) -> None:
        await self.session.delete(product_data)
        await self.session.commit()