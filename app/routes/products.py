from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Query, status
from app.core.database import session_db
from decimal import Decimal
from typing import Optional
from app.core.security import  locked_route, require_admin
from app.models.users import UserModel
from app.repositories.products import ProductRepository
from app.schemas.products import ProductDetailsSchema, ProductSchema
from app.services.products import ProductService

router = APIRouter(prefix="/products", tags=["products"])

def get_service(db: AsyncSession = Depends(session_db), locked: UserModel = Depends(locked_route)) -> ProductService:
    return ProductService(ProductRepository(db))


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=ProductDetailsSchema)
async def get_by_id(id: int, service: ProductService = Depends(get_service)):
    return await service.get_by_id(id)


@router.get("/", status_code=status.HTTP_200_OK)
async def list(
    limit: int = 10, offset: int = 0,
    section: Optional[str] = Query(None, description="Nome da seção que deseja filtrar", examples={"exemplo": {"section": "brinquedos"}}),
    price_min: Optional[Decimal] = Query(None, description="Preço mínimo para filtrar produtos", examples={"exemplo": {"price_min": "10.00"}}),
    price_max: Optional[Decimal] = Query(None, description="Preço maxímo para filtrar produtos", examples={"exemplo": {"price_max": "50.00"}}),
    availability: Optional[bool] = Query(None, description="Disponibilidade do produto", examples={"exemplo": {"availability": "true"}}),
    service: ProductService = Depends(get_service)
):
    return await service.list(limit, offset, section, price_min, price_max, availability)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductDetailsSchema)
async def create(data: ProductSchema, service: ProductService = Depends(get_service)):
    return await service.create(data)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=ProductDetailsSchema)
async def update(id: int, data: ProductSchema, service: ProductService = Depends(get_service)):
    return await service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, service: ProductService = Depends(get_service), admin: UserModel = Depends(require_admin)) -> None:
    await service.delete(id)