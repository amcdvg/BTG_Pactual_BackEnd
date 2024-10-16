import pytest
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from Router.getTransactions import getTransations
from Tools.convertDecimalFloat import convertDecimalFloat
from bson import ObjectId

# Fixture para mockear las transacciones
@pytest.fixture
def mock_transactions():
    return [
        {
            "id": str(ObjectId()),
            "amount": 100.50,
            "description": "Payment"
        },
        {
            "id": str(ObjectId()),
            "amount": 250.75,
            "description": "Refund"
        }
    ]

# Prueba para el caso exitoso
@pytest.mark.asyncio
async def test_get_transactions_success(mocker, mock_transactions):
    # Mock de la conexión a la tabla "Transactions"
    mock_transactions_table = mocker.patch('Router.getTransactions.connection')
    mock_transactions_table.return_value.scan.return_value = {
        'Items': mock_transactions
    }
    
    # Mockear la función de conversión
    mock_convert = mocker.patch('Router.getTransactions.convertDecimalFloat')
    mock_convert.return_value = mock_transactions

    # Llamar a la función con los valores mockeados
    response = await getTransations()

    assert response.status_code == 200
    response_data = response.body 
    assert response_data == response.body
    
# Prueba para el caso donde no se encuentran transacciones
@pytest.mark.asyncio
async def test_get_transactions_no_items(mocker):
    # Mock de la conexión a la tabla "Transactions"
    mock_transactions_table = mocker.patch('Router.getTransactions.connection')
    mock_transactions_table.return_value.scan.return_value = {'Items': []}

    # Llamar a la función y esperar un error 404
    with pytest.raises(HTTPException) as excinfo:
        await getTransations()

    assert excinfo.value.status_code == 500
    assert excinfo.value.detail == "An unexpected error occurred: 404: No items found"

# Prueba para el caso de excepción inesperada
@pytest.mark.asyncio
async def test_get_transactions_exception(mocker):
    # Mock de la conexión a la tabla "Transactions" que lanza una excepción
    mock_transactions_table = mocker.patch('Router.getTransactions.connection')
    mock_transactions_table.side_effect = Exception("Database connection error")

    # Verificar que se levante una HTTPException
    with pytest.raises(HTTPException) as excinfo:
        await getTransations()

    assert excinfo.value.status_code == 500
    assert "Database connection error" in excinfo.value.detail
