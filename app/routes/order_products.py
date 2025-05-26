from datetime import datetime
from decimal import Decimal
from typing import Optional
from app.models.users import UserModel
from app.core.database import session_db
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.orders import OrderRepository
from app.repositories.products import ProductRepository
from app.core.security import locked_route, require_admin
from app.schemas.order_products import OrderProductsDetailsSchema, OrderProductsSchema, OrderProductsUpdateSchema
from app.services.order_products import OrderProductsService
from app.repositories.order_products import OrderProductsRepository

router = APIRouter(prefix="/order-products", tags=["order-products"])

def get_service(db: AsyncSession = Depends(session_db), locked: UserModel = Depends(locked_route)) -> OrderProductsService:
    return OrderProductsService(OrderRepository(db), ProductRepository(db), OrderProductsRepository(db))

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=OrderProductsSchema)
async def get_by_id(id: int, service: OrderProductsService = Depends(get_service)):
    return await service.get_by_id(id)

@router.get(
    "/", 
    status_code=status.HTTP_200_OK, 
    response_model=list[OrderProductsDetailsSchema]
)
async def list(
    order_id: Optional[int] = Query(None,
        description="ID do pedido para filtrar itens",
        examples={"exemplo": {"order_id": 1}}
    ),
    
    product_id: Optional[int] = Query(None,
        description="ID do produto para filtrar itens",
        examples={"exemplo": {"product_id": 42}}
    ),
    
    quantity: Optional[int] = Query(None,
        description="Quantidade exata do item no pedido",
        examples={"exemplo": {"quantity": 3}}
    ),
    
    price_at_moment_min: Optional[Decimal] = Query(None,
        description="Preço mínimo do item no momento do pedido",
        examples={"exemplo": {"price_at_moment_min": "10.00"}}
    ),
    
    price_at_moment_max: Optional[Decimal] = Query(None,
        description="Preço máximo do item no momento do pedido",
        examples={"exemplo": {"price_at_moment_max": "50.00"}}
    ),
    
    date_start: Optional[datetime] = Query(None,
        description="Data inicial para filtrar itens (ISO 8601)",
        examples={"exemplo": {"date_start": "2025-01-01T00:00:00"}}
    ),
    
    date_end: Optional[datetime] = Query(None,
        description="Data final para filtrar itens (ISO 8601)",
        examples={"exemplo": {"date_end": "2025-01-31T23:59:59"}}
    ),
    
    service: OrderProductsService = Depends(get_service)
):
    return await service.list(
        order_id=order_id,
        product_id=product_id,
        quantity=quantity,
        price_at_moment_min=price_at_moment_min,
        price_at_moment_max=price_at_moment_max,
        date_start=date_start,
        date_end=date_end
    )

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderProductsSchema)
async def create(data: OrderProductsSchema, service: OrderProductsService = Depends(get_service)):
    return await service.create(data)

@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=OrderProductsSchema)
async def update(data: OrderProductsUpdateSchema, service: OrderProductsService = Depends(get_service)):
    return await service.update(data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, service: OrderProductsService = Depends(get_service), admin: UserModel = Depends(require_admin)):
    return await service.delete(id)