import pytest
from unittest.mock import patch, Mock
from botocore.exceptions import BotoCoreError, ClientError
from Data.data import connection  # Asegúrate de importar tu función correctamente

@patch('Data.data.boto3.resource')
@patch('Data.data.load_dotenv')
@patch('Data.data.os.getenv')
def test_connection(mock_getenv, mock_load_dotenv, mock_resource):
    # Configurar los mocks
    mock_getenv.side_effect = lambda key: {
        "AWSACCESSKEYID": "fake_access_key_id",
        "AWSSECRETACCESSKEY": "fake_secret_access_key",
        "AWSREGION": "fake_region"
    }.get(key)
    
    mock_table = Mock()
    mock_table.load.return_value = None  # Simular que la tabla se carga correctamente
    mock_resource.return_value.Table.return_value = mock_table

    # Llamar a la función con datos de prueba
    table = connection("testTable")

    # Verificar que los métodos correctos fueron llamados
    mock_load_dotenv.assert_called_once()
    mock_resource.assert_called_once_with(
        "dynamodb",
        aws_access_key_id="fake_access_key_id",
        aws_secret_access_key="fake_secret_access_key"
    )
    mock_resource.return_value.Table.assert_called_once_with("testTable")
    mock_table.load.assert_called_once()

    # Verificar que la tabla se devuelve correctamente
    assert table == mock_table

@patch('Data.data.boto3.resource')
@patch('Data.data.load_dotenv')
@patch('Data.data.os.getenv')
def test_connection_error(mock_getenv, mock_load_dotenv, mock_resource):
    # Configurar los mocks
    mock_getenv.side_effect = lambda key: {
        "AWSACCESSKEYID": "fake_access_key_id",
        "AWSSECRETACCESSKEY": "fake_secret_access_key",
        "AWSREGION": "fake_region"
    }.get(key)
    
    mock_table = Mock()
    mock_table.load.side_effect = ClientError({"Error": {"Code": "ResourceNotFoundException"}}, "load")
    mock_resource.return_value.Table.return_value = mock_table

    # Llamar a la función con datos de prueba
    result = connection("testTable")

    # Verificar que los métodos correctos fueron llamados
    mock_load_dotenv.assert_called_once()
    mock_resource.assert_called_once_with(
        "dynamodb",
        aws_access_key_id="fake_access_key_id",
        aws_secret_access_key="fake_secret_access_key"
    )
    mock_resource.return_value.Table.assert_called_once_with("testTable")
    mock_table.load.assert_called_once()

    # Verificar que se devuelve el error correctamente
    assert result == {"table": None, "error": "Error connecting to DynamoDB: An error occurred (ResourceNotFoundException) when calling the load operation: Unknown"}

