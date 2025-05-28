from fastapi import FastAPI
from app.routes import create_routes

def create_app() -> FastAPI:
    app = FastAPI(
        title="lu-fastapi-backend",
        version='1.0.0'
    )
    
    create_routes(instance_fastapi=app)

    return app