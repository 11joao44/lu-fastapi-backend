from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title="lu-fastapi-backend",
        version='1.0.0'
    )

    return app