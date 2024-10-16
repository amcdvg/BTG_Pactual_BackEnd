import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException
from Model.model import User
from bson import ObjectId
from boto3.dynamodb.conditions import Key
from datetime import datetime
from Router.userRegister import registerUser  # Asegúrate de importar correctamente tu función de ruta

@pytest.fixture
def mock_user():
    return User(
        email="test@example.com",
        hashedPassword="password123",
        fullName="Test User",
        phoneNumber="1234567890",
        isActive=True,
        isSuperuser=False,
        createdAt=datetime.now()
    )

@patch('Router.userRegister.ObjectId')
@patch('Router.userRegister.connection')
@patch('Router.userRegister.hashPasswordSha256')
@pytest.mark.asyncio
async def test_registerUser(mock_hashPasswordSha256, mock_connection, mock_objectId, mock_user):
    # Configurar los mocks
    mock_table = Mock()
    mock_connection.return_value = mock_table
    mock_table.query.return_value = {'Items': []}  # Simulando que no existe el usuario
    mock_hashPasswordSha256.return_value = "hashed_password"
    
    # Mock ObjectId to return a fixed value
    id_mock = "670e7891283b87d1302ec56e"
    mock_objectId.return_value = id_mock
    
    # Llamar a la función con datos de prueba
    response = await registerUser(mock_user)
    print(type(response))
    # Verificar que los métodos correctos fueron llamados
    mock_connection.assert_called_once_with("Users")
    mock_table.query.assert_called_once_with(
        IndexName='EmailIndex',
        KeyConditionExpression=Key('email').eq(mock_user.email)
    )
    mock_hashPasswordSha256.assert_called_once_with(mock_user.hashedPassword)
    mock_objectId.assert_called_once()  # Verifica que ObjectId se haya llamado
    
    mock_table.put_item.assert_called_once_with(Item={
        "id": id_mock,
        "email": mock_user.email,
        "hashedPassword": "hashed_password",
        "fullName": mock_user.fullName,
        "phoneNumber": mock_user.phoneNumber,
        "isActive": mock_user.isActive,
        "isSuperuser": mock_user.isSuperuser,
        "createdAt": mock_user.createdAt.isoformat()
    })
    print({"email": mock_user.email, "id":id_mock})
    # Verificar que la respuesta sea correcta
    assert response == {"email": mock_user.email, "id": response["id"]}

@patch('Router.userRegister.connection')
@pytest.mark.asyncio
async def test_registerUser_existing_email(mock_connection, mock_user):
    # Configurar los mocks
    mock_table = Mock()
    mock_connection.return_value = mock_table
    mock_table.query.return_value = {'Items': [mock_user]}  # Simulando que el usuario ya existe

    # Verificar que se lanza una excepción HTTP 400
    with pytest.raises(HTTPException) as exc_info:
        await registerUser(mock_user)
    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "An unexpected error occurred: 400: Email already registered"
