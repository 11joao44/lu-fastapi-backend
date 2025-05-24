from fastapi import FastAPI
from app.routes.users import router as auth_router
from app.routes.clients import router as router_clients

def create_routes(instance_fastapi: FastAPI) -> None:
        
        @instance_fastapi.get('/')
        def home():
                return "API RODANDO"

        instance_fastapi.include_router(auth_router)
        instance_fastapi.include_router(router_clients)
