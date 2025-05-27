from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import BaseRepository
from sqlalchemy.orm import DeclarativeBase
from fastapi import HTTPException, status
from typing import Optional

async def get_by_id_or_404(session: AsyncSession, model: DeclarativeBase, id: Optional[int]) -> DeclarativeBase:
    repository = BaseRepository(session, model).get_by_field("id", id)
    if repository is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.nome} referente ao ID: {id} não encontrado."
        )
