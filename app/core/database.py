from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship # relationship usado p/ importar em models
from app.core.config import settings

Base = declarative_base()

engine = create_async_engine(settings.DATABASE_URL, echo=True, future=True)

async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def session_db():
    async with async_session_maker() as session:
        yield session