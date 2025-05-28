import pytest
from app.services.users import UserService
from app.schemas.users import UserRegister
from unittest.mock import AsyncMock

@pytest.mark.asyncio
async def test_create_user_success():
    # Arrange
    mock_repo = AsyncMock()
    mock_repo.get_by_email.return_value = None  # Simula que o e-mail ainda não existe
    mock_repo.create.return_value = "USER OBJETO FAKE"  # Simule o retorno que quiser

    service = UserService(mock_repo)
    user_data = UserRegister(username="teste", email="teste@email.com", password="minhasenha123")

    # Act
    result = await service.create(user_data)

    # Assert
    assert result == "USER OBJETO FAKE"
    mock_repo.get_by_email.assert_called_once_with("teste@email.com")
    mock_repo.create.assert_called_once()
