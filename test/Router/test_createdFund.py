import pytest
from fastapi.testclient import TestClient
from Router.createdFund import appFunds, Fund
from moto import mock_dynamodb2
from pydantic import ValidationError
import boto3
from unittest.mock import patch
from botocore.exceptions import ClientError 

client = TestClient(appFunds)

# Definir la función de prueba para agregar un fondo
@mock_dynamodb2
def test_add_fund():
    # Configurar la simulación de DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    
    # Crear la tabla simulada
    table = dynamodb.create_table(
        TableName='Funds',
        KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'id',
                'AttributeType': 'S'
            },
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )

    # Definir el payload para la prueba
    payload = {
        "name": "Test Fund",
        "minimumAmount": 1000,
        "category": "Equity"
    }

    # Enviar una solicitud POST al endpoint
    response = client.post("/addFund/", json=payload)

    # Afirmar que el código de estado de la respuesta es 200
    assert response.status_code == 200

    # Afirmar el contenido de la respuesta
    data = response.json()
    assert data["Fondo"] == "Test Fund"
    assert "id" in data

    # Verificar que el fondo se haya agregado correctamente
    added_fund = table.get_item(Key={'id': data["id"]})
    assert 'Item' in added_fund
    assert added_fund['Item']['name'] == payload['name']

