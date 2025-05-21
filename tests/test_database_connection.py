import pytest
from sqlalchemy import text
from app.core.database import engine

def test_database_connection():
    """
    Testa se é possível conectar e executar uma query simples no banco de dados.
    """
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            assert result.scalar() == 1
    except Exception as e:
        pytest.fail(f"Erro ao conectar no banco: {e}")
