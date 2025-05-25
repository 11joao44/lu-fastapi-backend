from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import UserModel
from app.repositories.clients import ClientRepository
from app.repositories.orders import OrderRepository
from app.repositories.users import UserRepository
from app.services.orders import OrderService
from app.schemas.orders import OrderDetailsSchema, OrderSchema
from app.core.database import session_db
from app.core.security import require_admin

router = APIRouter(prefix="/orders", tags=["orders"])

def get_service(db: AsyncSession = Depends(session_db)) -> OrderService:
    return OrderService(OrderRepository(db), UserRepository(db), ClientRepository(db))

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderDetailsSchema)
async def register_order_route(order_data: OrderSchema, service: OrderService = Depends(get_service)):
    return await service.register_order_service(order_data)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrderDetailsSchema])
async def list_orders_route(
    date_start: Optional[datetime] = None,
    date_end: Optional[datetime] = None,
    product_id: Optional[int] = None,
    client_id: Optional[int] = None,
    section: Optional[str] = None,
    status: Optional[str] = None,
    service: OrderService = Depends(get_service)
):
    return await service.list_orders_service(date_start, date_end, product_id, client_id, section, status)

@router.get("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderDetailsSchema)
async def list_order_route(order_id: int, service: OrderService = Depends(get_service)):
    return await service.list_order_service(order_id)

@router.put("/{order_id}", status_code=status.HTTP_200_OK, response_model=OrderDetailsSchema)
async def update_order_route(order_id: int, order_data: OrderSchema, service: OrderService = Depends(get_service)):
    return await service.update_order_service(order_id, order_data)

@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order_route(order_id: int, service: OrderService = Depends(get_service), admin: UserModel = Depends(require_admin)):
    return await service.delete_order_service(order_id)