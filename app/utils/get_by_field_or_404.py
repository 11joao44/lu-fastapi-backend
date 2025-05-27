from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import BaseRepository
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from typing import List, Type

async def get_by_field_or_404(
    session: AsyncSession,
    model: Type[DeclarativeBase],
    columns: List[str],
    data: BaseModel
) -> None:
    """
    Verifica se algum dos campos passados em 'columns' já está cadastrado no banco.
    Lança HTTP 409 se encontrar duplicidade.
    """
    repository = BaseRepository(session, model)
    for column in columns:
        value = getattr(data, column)
        if await repository.get_by_field(column, value):
            raise HTTPException(status.HTTP_409_CONFLICT, f"{column} já cadastrado.")
