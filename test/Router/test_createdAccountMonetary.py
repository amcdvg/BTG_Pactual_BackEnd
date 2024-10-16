import pytest
from fastapi.testclient import TestClient
from Router.createdAccountMonetary import appAccountMonetary,accountMonetary
from Model.model import AccountMonetary
from unittest.mock import patch
from bson import ObjectId
from datetime import datetime
from fastapi import HTTPException

# Crear cliente de pruebas
client = TestClient(appAccountMonetary)

# Simular datos para la cuenta
@pytest.fixture
def mock_account():
    return AccountMonetary(
        amount=100.0,
        createdAt=datetime.utcnow()
    )

@pytest.fixture
def mock_user_response():
    return {
        "Items": [
            {
                "id": str(ObjectId()),
                "email": "test@example.com"
            }
        ]
    }

# Prueba para el caso exitoso
@pytest.mark.asyncio
async def test_account_monetary_success(mocker, mock_account, mock_user_response):
    # Mock de la conexión a la tabla "Users"
    mock_users_table = mocker.patch('Router.createdAccountMonetary.connection')
    mock_users_table.return_value.query.return_value = mock_user_response

    # Mock de la conexión a la tabla "AccountMonetary"
    mock_account_table = mocker.patch('Router.createdAccountMonetary.connection')
    mock_account_table.return_value.put_item.return_value = None  # put_item no retorna nada

    # Llamar a la función con los valores mockeados
    response = await accountMonetary(mock_account, "test@example.com")

    assert response["status"] == 200
    assert response["message"] == "Operation was successful"
    

# Prueba para cuando ocurre una excepción
@pytest.mark.asyncio
async def test_account_monetary_exception(mocker, mock_account):
    # Simular un error al obtener los datos del usuario
    mock_users_table = mocker.patch('Router.createdAccountMonetary.connection')
    mock_users_table.return_value.query.side_effect = Exception("DB error")

    # Verificar que se levante una HTTPException
    with pytest.raises(HTTPException) as excinfo:
        await accountMonetary(mock_account, "test@example.com")

    assert excinfo.value.status_code == 500
    assert "An unexpected error occurred" in str(excinfo.value.detail)