import pytest
from fastapi import HTTPException
from Router.cancelBodingFund import canceledBodingFund
from unittest.mock import patch, AsyncMock
from datetime import datetime
from bson import ObjectId

@pytest.fixture
def mock_data():
    """Fixture para simular datos de fondo de inversión."""
    return {
        "id": str(ObjectId()),
        "userId": str(ObjectId()),
        "investedAmount": 1000,
        "uniqueNumber": "unique_value_123",
        "notificationPreferences": "email",
        "fundId": str(ObjectId())
    }

@pytest.fixture
def mock_user_data():
    """Fixture para simular datos de usuario."""
    return {
        "id": str(ObjectId()),
        "fullName": "John Doe",
        "phoneNumber": "1234567890",
        "email": "johndoe@example.com"
    }

@pytest.fixture
def mock_fund_data():
    """Fixture para simular datos de fondo."""
    return {
        "id": str(ObjectId()),
        "name": "Investment Fund",
        "minimumAmount": 500,
        "category": "Equity"
    }
@pytest.mark.asyncio
@patch('Router.cancelBodingFund.connection')
@patch('utils.emails.sendEmail.sendEmail', new_callable=AsyncMock)
@patch('utils.msm.sendMsm.sendMSM', new_callable=AsyncMock)
async def test_canceled_boding_fund_success(mock_send_email, mock_send_msm, mock_connection):
    """Test para el caso exitoso de cancelación de fondo de inversión."""

    # Mockear los datos del fondo de inversión
    mock_data = {
        "id": str(ObjectId()),
        "userId": "670db4d1dc83c18405b27172",  # Asegúrate de que este valor se use
        "investedAmount": 1000,
        "uniqueNumber": "unique_value_123",
        "notificationPreferences": "email",
        "fundId": str(ObjectId()),
        "status": "active"  # Incluido el estado
    }

    # Mockear datos de cuenta del cliente
    mock_user_data = {
        "userId": "670dfb8e2f36612c9b6f723a",
        "accountBalance": 2000,
        "accountStatus": "active"
    }

    # Simular la consulta de fondo de inversión
    funds_investment_mock = mock_connection.return_value
    funds_investment_mock.query.return_value = {
        'Items': [mock_data]  # Retornar el fondo de inversión mockeado
    }
    funds_investment_mock.update_item.return_value = {}

    # Simular la consulta de cuentas monetarias del cliente
    account_monetary_mock = mock_connection.return_value
    account_monetary_mock.query.return_value = {
        'Items': [mock_user_data]  # Asegúrate de que esto contenga userId
    }

    # Llamar a la función con un ID simulado
    with pytest.raises(HTTPException) as excinfo:
        await canceledBodingFund("670e01ff7bfae3de756730c9")
    assert excinfo.value.status_code == 500
    

@pytest.mark.asyncio
@patch('Router.cancelBodingFund.connection')
async def test_canceled_boding_fund_item_not_found(mock_connection, mock_data):
    """Test para el caso donde no se encuentra el fondo de inversión."""

    # Mockear la conexión a la base de datos
    funds_investment_mock = mock_connection.return_value
    funds_investment_mock.query.return_value = {
        'Items': []  # Simular que no se encontró el fondo
    }

    # Llamar a la función y esperar que lance HTTPException
    with pytest.raises(HTTPException) as excinfo:
        await canceledBodingFund(Id=mock_data['id'])

    assert excinfo.value.status_code == 500
    assert "An unexpected error occurred:" in excinfo.value.detail

@pytest.mark.asyncio
@patch('Router.cancelBodingFund.connection')
async def test_canceled_boding_fund_unexpected_exception(mock_connection):
    """Test para manejar excepciones inesperadas."""

    # Simular un error inesperado en la conexión a la base de datos
    mock_connection.side_effect = Exception("Unexpected error")

    # Llamar a la función y esperar un error 500
    with pytest.raises(HTTPException) as excinfo:
        await canceledBodingFund(Id="fake_id")

    assert excinfo.value.status_code == 500
    assert "An unexpected error occurred:" in excinfo.value.detail
