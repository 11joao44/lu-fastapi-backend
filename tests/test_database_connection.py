import pytest
from sqlalchemy import text
from app.core.database import engine

@pytest.mark.asyncio
async def test_database_connection() -> None:
    """
    Testa se é possível conectar e executar uma query simples no banco de dados.
    Ideal para health check da infra de testes.
    """
    try:
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            assert result.scalar_one() == 1
    except Exception as e:
        pytest.fail(f"Erro ao conectar no banco: {e}")