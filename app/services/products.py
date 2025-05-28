from typing import Optional
from decimal import Decimal
from app.models.products import ProductModel
from app.repositories.products import ProductRepository
from app.schemas.products import ProductSchema, ProductUpdateSchema
from app.utils.fecth_by_id_or_404 import fecth_by_id_or_404
from fastapi import HTTPException, status

class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo
    
    async def get_by_id(self, id: int) -> ProductModel:
        return await fecth_by_id_or_404(self.product_repo.session, ProductModel, id)
    
    async def list(self, 
        limit: int,
        offset: int,
        section: Optional[str],
        price_min: Optional[Decimal],
        price_max: Optional[Decimal],
        availability: Optional[str]
    ) -> ProductModel:
        return await self.product_repo.list(limit, offset, section, price_min, price_max, availability)
    
    async def create(self, data: ProductSchema) -> ProductModel:
        
        if await self.product_repo.get_by_barcode(data.barcode):
            raise HTTPException(status.HTTP_409_CONFLICT, f"Produto referente ao barcode: {data.barcode} já foi cadastrado.")
    
        product = ProductModel(
            name=data.name,
            description=data.description,
            price=data.price,
            barcode=data.barcode,
            section=data.section,
            stock=data.stock,
            expiration_date=data.expiration_date,
            image_url=data.image_url
        )
    
        return await self.product_repo.create(product)
    
    async def update(self, id: int, update_data: ProductUpdateSchema) -> ProductModel:
        db_instance = await fecth_by_id_or_404(self.product_repo.session, ProductModel, id)
        return await self.product_repo.update(db_instance, update_data)
    
    async def delete(self, id: int) -> None:
        data = await fecth_by_id_or_404(self.product_repo.session, ProductModel, id)
        await self.product_repo.delete(data)