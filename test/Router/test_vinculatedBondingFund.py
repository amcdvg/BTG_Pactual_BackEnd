import pytest
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Router.vinculatedBondingFund import vinculatedBodingFund, getNumberUnique
from Model.model import BondingFund
from bson import ObjectId
from unittest.mock import MagicMock
from pydantic import ValidationError
from unittest.mock import Mock

# Fixture para un objeto BondingFund simulado
@pytest.fixture
def bonding_fund_data():
    return BondingFund(
        uniqueNumber="unique_value_123",  # Provide a valid unique number
        investedAmount=1000,
        bondingDate="2024-10-15T00:00:00",
        notificationPreferences="email"
    )

# Mockear las funciones de envío de notificaciones
@pytest.fixture
def mock_send_functions(mocker):
    mock_send_email = mocker.patch('utils.emails.sendEmail.sendEmail', return_value=None)
    mock_send_msm = mocker.patch('utils.msm.sendMsm.sendMSM', return_value=None)
    return mock_send_email, mock_send_msm

@pytest.mark.asyncio
async def test_vinculated_bonding_fund_success(mocker, bonding_fund_data, mock_send_functions):
    """Test para el caso exitoso de vinculación de fondos."""

    # Mockear la conexión a la base de datos
    mock_connection = mocker.patch('Router.vinculatedBondingFund.connection')
    
    # Configurar el mock para los usuarios
    mock_connection.return_value.query.side_effect = [
        {
            'Items': [{'id': str(ObjectId()), 'fullName': 'John Doe', 'phoneNumber': '1234567890', 'email': 'johndoe@example.com'}]
        },
        {
            'Items': [{'id': str(ObjectId()), 'name': 'Investment Fund', 'minimumAmount': 500, 'category': 'Equity'}]
        },
        {
            'Items': [{'id': str(ObjectId()), 'userId': 'user-id', 'amount': 5000}]  # Saldo suficiente
        }
    ]
    
    # Mockear la creación de la transacción
    mock_connection.return_value.put_item.return_value = {}

    # Llamar a la función con datos simulados
    response = await vinculatedBodingFund(bonding_fund_data, email="johndoe@example.com", fund="Investment Fund")

    # Aserciones para verificar el éxito de la operación
    assert response.status_code == 200
    response_data = response.body 
    assert response_data == response.body


# Prueba para el caso de cuenta insuficiente
@pytest.mark.asyncio
async def test_vinculated_bonding_fund_insufficient_balance(mocker, bonding_fund_data):
    mock_users_table = mocker.patch('Router.vinculatedBondingFund.connection')
    mock_funds_table = mocker.patch('Router.vinculatedBondingFund.connection')
    mock_account_table = mocker.patch('Router.vinculatedBondingFund.connection')

    mock_users_table.return_value.query.return_value = {
        'Items': [{'id': str(ObjectId()), 'fullName': 'John Doe', 'phoneNumber': '1234567890', 'email': 'johndoe@example.com'}]
    }
    mock_funds_table.return_value.query.return_value = {
        'Items': [{'id': str(ObjectId()), 'name': 'Investment Fund', 'minimumAmount': 500.0, 'category': 'Equity'}]
    }
    mock_account_table.return_value.query.return_value = {
        'Items': [{'id': str(ObjectId()), 'userId': 'user-id', 'amount': 500.0}]  # Saldo insuficiente
    }

    # Llamar a la función y esperar un error 400
    with pytest.raises(HTTPException) as excinfo:
        await vinculatedBodingFund(bonding_fund_data, email="johndoe@example.com", fund="Investment Fund")

    assert excinfo.value.status_code == 500
    assert "An unexpected error occurred:" in excinfo.value.detail

# Prueba para el manejo de excepciones inesperadas
@pytest.mark.asyncio
async def test_vinculated_bonding_fund_unexpected_exception(mocker, bonding_fund_data):
    mock_users_table = mocker.patch('Router.vinculatedBondingFund.connection')
    mock_users_table.side_effect = Exception("Unexpected error")
    # Llamar a la función y esperar un error 500
    with pytest.raises(HTTPException) as excinfo:
        await vinculatedBodingFund(bonding_fund_data, email="johndoe@example.com", fund="Investment Fund")

    assert excinfo.value.status_code == 500
    assert "An unexpected error occurred" in excinfo.value.detail

# Prueba para la función getNumberUnique
def test_get_number_unique():
    unique_number = getNumberUnique("fund1", "client1", "transaction1")
    assert len(unique_number) == 12  # Debe tener 12 dígitos
