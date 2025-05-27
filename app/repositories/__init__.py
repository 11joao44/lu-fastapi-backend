from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from sqlalchemy import select
from typing import Any, Type

class BaseRepository:
    def __init__(self, session: AsyncSession, model: Type[DeclarativeBase]):
        self.session = session
        self.model = model
    
    async def get_by_field(self, column: str, value: Any) -> DeclarativeBase | None:
        """Busca a primeira instância do modelo pelo campo informado."""
        result = await self.session.execute(
            select(self.model).where(getattr(self.model, column) == value)
        )
        return result.scalar_one_or_none()
    
    async def create(self, data: DeclarativeBase) -> DeclarativeBase:
        """Adiciona e retorna uma nova instância no banco."""
        self.session.add(data)
        await self.session.commit()
        await self.session.refresh(data)
        return data
    
    async def update(self, db_instance: DeclarativeBase, update_date: BaseModel) -> DeclarativeBase:
        """Atualiza os campos da instância com base em um schema Pydantic."""
        for key, value in update_date.model_dump(exclude_unset=True).items():
            setattr(db_instance, key, value)
        await self.session.commit()
        await self.session.refresh(db_instance)
        return db_instance
    
    def ola():
        pass
    
    async def delete(self, data: DeclarativeBase) -> None:
        """Remove uma instância do banco."""
        await self.session.delete(data)
        await self.session.commit()