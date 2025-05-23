from fastapi import FastAPI
from app.routes.auth_routes import router as auth_router

def create_routes(instance_fastapi: FastAPI) -> None:
        
        @instance_fastapi.get('/')
        def home():
                return "API RODANDO"

        instance_fastapi.include_router(auth_router)
