import pytest
from unittest.mock import patch, Mock
from Tools.createdTable import createTable  # Asegúrate de importar tu función correctamente

@patch('Tools.createdTable.resource')
@patch('Tools.createdTable.load_dotenv')
@patch('Tools.createdTable.os.getenv')
def test_createTable(mock_getenv, mock_load_dotenv, mock_resource):
    # Configurar los mocks
    mock_getenv.side_effect = lambda key: {
        "AWSACCESSKEYID": "fake_access_key_id",
        "AWSSECRETACCESSKEY": "fake_secret_access_key",
        "AWSREGION": "fake_region"
    }.get(key)
    
    mock_dynamodb = Mock()
    mock_table = Mock()
    mock_dynamodb.create_table.return_value = mock_table
    mock_resource.return_value = mock_dynamodb

    # Llamar a la función con datos de prueba
    createTable("testTable", "testKey")

    # Verificar que los métodos correctos fueron llamados
    mock_load_dotenv.assert_called_once()
    mock_resource.assert_called_once_with(
        "dynamodb",
        aws_access_key_id="fake_access_key_id",
        aws_secret_access_key="fake_secret_access_key"
    )
    mock_dynamodb.create_table.assert_called_once_with(
        TableName="testTable",
        KeySchema=[
            {
                'AttributeName': "testKey",
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': "testKey",
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )
