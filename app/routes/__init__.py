from fastapi import FastAPI
from app.routes.users import router as router_users
from app.routes.orders import router as router_orders
from app.routes.clients import router as router_clients
from app.routes.products import router as router_products
from app.routes.order_products import router as router_order_products

def create_routes(instance_fastapi: FastAPI) -> None:
        
        @instance_fastapi.get('/')
        def home(): return {"details": "Olá, FastAPI está funcionando!"}

        instance_fastapi.include_router(router_users)
        instance_fastapi.include_router(router_orders)
        instance_fastapi.include_router(router_clients)
        instance_fastapi.include_router(router_products)
        instance_fastapi.include_router(router_order_products)
