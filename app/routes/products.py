from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, status
from app.core.database import session_db
from decimal import Decimal
from typing import Optional

from app.core.security import require_admin
from app.models.users import UserModel
from app.repositories.products import ProductRepository
from app.schemas.products import ProductDetailsSchema, ProductSchema
from app.services.products import ProductService

router = APIRouter(prefix="/products", tags=["products"])


def get_service(db: AsyncSession = Depends(session_db)) -> ProductService:
    return ProductService(ProductRepository(db))


@router.get("/", status_code=status.HTTP_200_OK)
async def list_products_route(
    limit: int = 10, offset: int = 0,
    section: Optional[str] = Query(None, description="Nome da seção que deseja filtrar", examples={"exemplo": {"section": "brinquedos"}}),
    price_min: Optional[Decimal] = Query(None, description="Preço mínimo para filtrar produtos", examples={"exemplo": {"price_min": "10.00"}}),
    price_max: Optional[Decimal] = Query(None, description="Preço maxímo para filtrar produtos", examples={"exemplo": {"price_max": "50.00"}}),
    availability: Optional[bool] = Query(None, description="Disponibilidade do produto", examples={"exemplo": {"availability": "true"}}),
    service: ProductService = Depends(get_service)
):
    return await service.list_products_service(limit, offset, section, price_min, price_max, availability)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductDetailsSchema)
async def register_product_route(product_data: ProductSchema, service: ProductService = Depends(get_service)):
    return await service.register_product_service(product_data)


@router.get("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductDetailsSchema)
async def list_product_route(product_id: int, service: ProductService = Depends(get_service)):
    return await service.list_product_service(product_id)


@router.put("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductDetailsSchema)
async def list_product_route(
    product_id: int, 
    product_data: ProductSchema, 
    service: ProductService = Depends(get_service)
):
    return await service.update_product_service(product_id, product_data)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def list_product_route(
    product_id: int, 
    service: ProductService = Depends(get_service), 
    current_user: UserModel = Depends(require_admin)
) -> None:
    await service.delete_product_service(product_id)