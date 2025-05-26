from app.models.users import UserModel
from app.core.database import session_db
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.orders import OrderRepository
from app.repositories.products import ProductRepository
from app.core.security import locked_route, require_admin
from app.schemas.order_products import OrderProductsSchema, OrderProductsUpdateSchema
from app.services.order_products import OrderProductsService
from app.repositories.order_products import OrderProductsRepository

router = APIRouter(prefix="/order-products", tags=["order-products"])

def get_service(db: AsyncSession = Depends(session_db), locked: UserModel = Depends(locked_route)) -> OrderProductsService:
    return OrderProductsService(OrderRepository(db), ProductRepository(db), OrderProductsRepository(db))

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=OrderProductsSchema)
async def get_by_id(id: int, service: OrderProductsService = Depends(get_service)):
    return await service.get_by_id(id)

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[OrderProductsSchema])
async def list(data: OrderProductsSchema, service: OrderProductsService = Depends(get_service)):
    return await service.list(data)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OrderProductsSchema)
async def create(data: OrderProductsSchema, service: OrderProductsService = Depends(get_service)):
    return await service.create(data)

@router.patch("/{id}", status_code=status.HTTP_200_OK, response_model=OrderProductsSchema)
async def update(data: OrderProductsUpdateSchema, service: OrderProductsService = Depends(get_service)):
    return await service.update(data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(id: int, data: OrderProductsSchema, service: OrderProductsService = Depends(get_service), admin: UserModel = Depends(require_admin)):
    return await service.delete(id, data)