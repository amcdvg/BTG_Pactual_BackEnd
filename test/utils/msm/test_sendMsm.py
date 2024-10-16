import os
import pytest
from unittest.mock import patch, Mock
from utils.msm.sendMsm import sendMSM  # Asegúrate de que este import esté correcto

@patch('utils.msm.sendMsm.Client')
@patch('utils.msm.sendMsm.load_dotenv')
@patch('os.getenv')  # Cambiado a os.getenv
def test_sendMSM(mock_getenv, mock_load_dotenv, mock_client):
    # Configurar los mocks
    mock_getenv.side_effect = lambda key: {
        "ACCOUNTSID": "fake_account_sid",
        "AUTHTOKEN": "fake_auth_token",
        "PHONENUMBERTWILIO": "+1234567890"
    }.get(key)
    
    mock_message = Mock()
    mock_message.sid = "fake_sid"
    mock_client.return_value.messages.create.return_value = mock_message

    # Llamar a la función con datos de prueba
    response = sendMSM("Hello, World!", "+0987654321")

    # Verificar que la respuesta sea correcta
    assert response.status_code == 200
    assert response.body == b'{"message":"SMS send Successfully!"}'  # Cambia content a body

    # Verificar que los métodos correctos fueron llamados
    mock_load_dotenv.assert_called_once()
    mock_client.assert_called_once_with("fake_account_sid", "fake_auth_token")
    mock_client.return_value.messages.create.assert_called_once_with(
        body="Hello, World!",
        from_="+1234567890",
        to="+0987654321"
    )
