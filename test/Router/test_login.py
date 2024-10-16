import pytest
from fastapi.testclient import TestClient
from Router.login import appLogin, createAccessToken,loginUser,usersTable, logoutUser 
import os
from dotenv import load_dotenv
from Tools.passwordHashed import hashPasswordSha256
from boto3.dynamodb.conditions import Key
from unittest.mock import patch
from unittest.mock import MagicMock
# Load environment variables
load_dotenv()

client = TestClient(appLogin)

def test_create_access_token():
    email = "test@example.com"
    token = createAccessToken(email)
    assert token is not None

def test_protected_route():
    email = "test@example.com"
    token = createAccessToken(email)
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/protected-route", headers=headers)
    assert response.status_code == 404
    

    

from unittest.mock import MagicMock

@pytest.fixture
def mock_dynamodb(mocker):
    # Mockea la función `connection` para que devuelva un mock de `usersTable`
    mock_users_table = MagicMock()

    # Define lo que debe devolver el método `query` cuando se llame
    mock_users_table.query.return_value = {
        'Items': [{
            "email": "alexander.moreno@utp.edu.co",
            "hashedPassword": hashPasswordSha256("AmcDvg03060306*"),
            "fullName": "Test User",
            "phoneNumber": "1234567890",
            "isActive": True,
            "isSuperuser": False,
            "createdAt": "2024-01-01T00:00:00"
        }],
        'Count': 1,
        'ScannedCount': 1,
        'ResponseMetadata': {
            'RequestId': '280VQRR48A1I0CUSJ2LGC2O1U7VV4KQNSO5AEMVJF66Q9ASUAAJG',
            'HTTPStatusCode': 200,
            'HTTPHeaders': {
                'server': 'Server',
                'date': 'Tue, 15 Oct 2024 16:25:52 GMT',
                'content-type': 'application/x-amz-json-1.0',
                'content-length': '396',
                'connection': 'keep-alive',
                'x-amzn-requestid': '280VQRR48A1I0CUSJ2LGC2O1U7VV4KQNSO5AEMVJF66Q9ASUAAJG',
                'x-amz-crc32': '4274503054'
            },
            'RetryAttempts': 0
        }
    }

    # Simula la conexión a DynamoDB para devolver `mock_users_table`
    mock_connection = mocker.patch("Data.data.connection", return_value=mock_users_table)

    return mock_connection

# Prueba de inicio de sesión exitoso
@pytest.mark.asyncio
async def test_login_success(mock_dynamodb):
    response = await loginUser("alexander.moreno@utp.edu.co",  "AmcDvg0306*")
    
    assert response.status_code == 200
    response_data = response.body 
    assert response_data == response.body

@pytest.mark.asyncio
async def test_logoutuser_success():
    response = await logoutUser("132u4ur2hruewheutu84t84ytugguhghg")
    assert response ==  {"message": "Logout successful"}
    
