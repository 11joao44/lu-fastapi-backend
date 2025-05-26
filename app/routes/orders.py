from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.users import UserModel
from app.repositories.clients import ClientRepository
from app.repositories.orders import OrderRepository
from app.repositories.users import UserRepository
from app.services.orders import OrderService
from app.schemas.orders import OrderDetailsSchema, OrderSchema
from app.core.database import session_db
from app.core.security import locked_route, require_admin

router = APIRouter(prefix="/orders", tags=["orders"])

def get_service(db: AsyncSession = Depends(session_db), locked: UserModel = Depends(locked_route)) -> OrderService:
    return OrderService(OrderRepository(db), UserRepository(db), ClientRepository(db))


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=OrderDetailsSchema)
async def get_by_id(id: int, service: OrderService = Depends(get_service)):
    return await service.get_by_id(id)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrderDetailsSchema])
async def list(
    date_start:  Optional[datetime] = Query(None, 
        description="Data inicial para filtrar registros (formato ISO 8601)", 
        examples={"exemplo": {"date_start": "2024-01-01T00:00:00"}}
    ),

    date_end: Optional[datetime] = Query(None, 
        description="Data final para filtrar registros (formato ISO 8601)",
        examples={"exemplo": {"date_end": "2024-01-31T23:59:59"}}
    ),

    product_id: Optional[int] = Query( None, 
        description="ID do produto que deseja filtrar",
        examples={"exemplo": {"product_id": 123}}
    ),

    client_id: Optional[int] = Query(None, 
        description="ID do cliente que deseja filtrar",
        examples={"exemplo": {"client_id": 456}}
    ),

    section: Optional[str] = Query(None, 
        description="Seção ou categoria que deseja filtrar",
        examples={"exemplo": {"section": "Financeiro"}}
    ),

    status: Optional[str] = Query(None, 
        description="Status da movimentação que deseja filtrar",
        examples={"exemplo": {"status": "Concluído"}}
    ),
    service: OrderService = Depends(get_service)
):
    return await service.list(date_start, date_end, product_id, client_id, section, status)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderDetailsSchema)
async def create(data: OrderSchema, service: OrderService = Depends(get_service)):
    return await service.create(data)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=OrderDetailsSchema)
async def update(id: int, data: OrderSchema, service: OrderService = Depends(get_service)):
    return await service.update(id, data)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, service: OrderService = Depends(get_service), admin: UserModel = Depends(require_admin)):
    return await service.delete(id)