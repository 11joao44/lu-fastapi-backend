from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import BaseRepository
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from typing import List, Optional, Type

async def check_unique_fields(
    schema: Type[BaseModel],
    session: AsyncSession,
    model: Type[DeclarativeBase],
    data: BaseModel,
    ignore: Optional[List[str]] = [],
    ) -> None:
    """
    ## Função `check_unique_fields`

    Verifica de forma assíncrona se algum campo de um `schema` já existe no banco de dados e, em caso de duplicidade, interrompe a requisição com um erro HTTP 409.

    ---

    **Parâmetros**
    - `schema: Type[BaseModel]`  
    Modelo Pydantic que define os campos a serem validados (usa `schema.model_fields.keys()`).

    - `session: AsyncSession`  
    Sessão assíncrona do SQLAlchemy usada para executar as queries de verificação.

    - `model: Type[DeclarativeBase]`  
    Classe ORM que representa a tabela onde serão feitas as consultas de existência.

    - `data: BaseModel`  
    Instância do schema contendo os valores informados pelo usuário a serem comparados.

    - `ignore: Optional[List[str]]`  
    Lista de campos que devem ser ignorados na verificação de duplicidade (padrão `[]`).

    **Retorno**
    - Lança `HTTPException() - 409 Conflict` ao detectar qualquer valor duplicado.
    - { "detail": "O email: user@email.com já foi cadastrado." }


    """
    repository = BaseRepository(session, model)
    for column in list(schema.model_fields.keys()):
        if column in ignore: continue

        value = getattr(data, column)
        if await repository.get_by_field(column, value):
            raise HTTPException(status.HTTP_409_CONFLICT, f"O {column}: {value} já foi cadastrado.")
