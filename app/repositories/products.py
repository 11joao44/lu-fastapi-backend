from sqlalchemy.ext.asyncio import AsyncSession
from app.models.products import ProductModel
from app.repositories import BaseRepository
from sqlalchemy import select
from typing import Optional
from decimal import Decimal

class ProductRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(session, ProductModel)
    
    async def get_by_barcode(self, barcode: str):
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.barcode == barcode)
        )
        return result.scalar_one_or_none()
    
    async def list(
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
