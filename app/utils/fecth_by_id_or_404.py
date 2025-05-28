from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import BaseRepository
from sqlalchemy.orm import DeclarativeBase
from fastapi import HTTPException, status
from typing import Optional

async def fecth_by_id_or_404(session: AsyncSession, model: DeclarativeBase, id: Optional[int]) -> DeclarativeBase:
    """
    Busca de forma assíncrona um registro pelo campo `id` e, se não encontrado,
    interrompe a requisição com um erro HTTP 404.

    **Parâmetros**
    - `session: AsyncSession`  
      Sessão assíncrona do SQLAlchemy usada para executar a query de busca.

    - `model: DeclarativeBase`  
      Classe ORM que representa a tabela onde será feita a consulta.

    - `id: Optional[int]`  
      Identificador do registro a ser buscado. Se for `None` ou não existir,
      será lançada uma exceção 404.

    **Retorno**
    - Retorna a instância de `model` correspondente ao `id` informado.  
    - Lança `HTTPException(status.HTTP_404_NOT_FOUND, ...)` se nenhum registro for encontrado.
    """
    data = await BaseRepository(session, model).get_by_field("id", id)
    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{model.nome} referente ao ID: {id} não encontrado."
        )
    return data
