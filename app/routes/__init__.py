from fastapi import FastAPI
from app.routes.user import users_routes

def create_routes(instance_fastapi: FastAPI) -> None:
    
    @instance_fastapi.get('/')
    def home():
        return "API RODANDO"
    
    users_routes(instance_fastapi)