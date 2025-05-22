import sys; import os; sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import text
from app.core.database import engine

@pytest.mark.asyncio
async def test_database_connection():
    """
    Testa se é possível conectar e executar uma query simples no banco de dados.
    """
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar_one() == 1
    except Exception as e:
        pytest.fail(f"Erro ao conectar no banco: {e}")
