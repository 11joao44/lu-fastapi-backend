from typing import Optional
from decimal import Decimal
from app.models.products import ProductModel
from app.repositories.products import ProductRepository
from app.schemas.products import ProductDetailsSchema, ProductSchema
from fastapi import HTTPException, status

def product_not_found(product: ProductModel) -> None:
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado")

class ProductService:
    def __init__(self, product_repo: ProductRepository):
        self.product_repo = product_repo

    async def list_products_service(self, 
        limit: int, offset: int, 
        section: Optional[str], 
        price_min: Optional[Decimal], 
        price_max: Optional[Decimal], 
        availability: Optional[str]
    ) -> ProductDetailsSchema:
        product = await self.product_repo.list_products_repository(limit, offset, section, price_min, price_max, availability)
        product_not_found(product)
        return product
    
    async def register_product_service(self, data: ProductSchema):
        if await self.product_repo.get_by_barcode(data.barcode):
            raise HTTPException(status.HTTP_409_CONFLICT, "Produto já foi cadastrado!.")
        
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

        return await self.product_repo.register_product_repository(product)
    
    async def list_product_service(self, product_id: int) -> ProductDetailsSchema:
        product = await self.product_repo.get_by_id(product_id)
        product_not_found(product)
        return product
    
    async def update_product_service(self, product_id: int, product_data: ProductSchema) -> ProductDetailsSchema:
        product = await self.product_repo.get_by_id(product_id)
        product_not_found(product)
        return await self.product_repo.update_product_repository(product, product_data)

    async def delete_product_service(self, product_id: int) -> None:
        product = await self.product_repo.get_by_id(product_id)
        product_not_found(product)
        await self.product_repo.delete_product_repository(product)