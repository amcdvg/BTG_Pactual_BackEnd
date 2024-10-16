import pytest
from unittest.mock import MagicMock
from utils.emails.sendEmail import CoreMailClient, sendEmail
from jinja2 import Template
from fastapi.responses import JSONResponse
import json


@pytest.fixture
def mock_smtp(mocker):
    return mocker.patch('smtplib.SMTP')


@pytest.fixture
def mock_ssl_context(mocker):
    return mocker.patch('ssl.create_default_context')


def test_send_email(mock_smtp, mock_ssl_context):
    # Mock context and SMTP server
    mock_context = MagicMock()
    mock_ssl_context.return_value = mock_context
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    # Create instance of the email client
    cm_client = CoreMailClient(
        smtp_server="smtp.gmail.com",
        port=587,
        sender_email="test_sender@gmail.com",
        password="password123",
        receiver_email=["receiver@example.com"],
        subject="Test Email",
        message="This is a test message.",
        from_name="Test Sender"
    )

    # Call the send_email method (no attachments)
    cm_client.send_email()

    # Assert that SMTP connection was made correctly
    mock_smtp.assert_called_with("smtp.gmail.com", 587)
    mock_server.starttls.assert_called_with(context=mock_context)
    mock_server.login.assert_called_with("test_sender@gmail.com", "password123")
    mock_server.sendmail.assert_called()


@pytest.fixture
def mock_mime_guess_type(mocker):
    return mocker.patch('mimetypes.guess_type', return_value=('application/pdf', None))


def test_create_message_application(mock_mime_guess_type, mocker):
    # Mock the file being opened
    mock_open = mocker.patch('builtins.open', mocker.mock_open(read_data=b'data'))

    cm_client = CoreMailClient(
        smtp_server="smtp.gmail.com",
        port=587,
        sender_email="test_sender@gmail.com",
        password="password123",
        receiver_email=["receiver@example.com"],
        subject="Test Email",
        message="This is a test message.",
        from_name="Test Sender"
    )

    # Call the method to create an attachment
    attachment = cm_client.create_message_application("dummy_path.pdf")

    # Assert the attachment has the correct MIME type
    assert attachment.get_content_type() == 'application/pdf'
    assert "Content-Disposition" in attachment


@pytest.fixture
def mock_render(mocker):
    return mocker.patch('jinja2.Template.render', return_value="Rendered HTML Message")


@pytest.fixture
def mock_open_file(mocker):
    return mocker.patch('builtins.open', mocker.mock_open(read_data="Template Content"))


@pytest.fixture
def mock_send_email_method(mocker):
    return mocker.patch('utils.emails.sendEmail.CoreMailClient.send_email')


def test_send_email_function(mock_open_file, mock_render, mock_send_email_method):
    # Call the sendEmail function
    response = sendEmail("Test User", "Notification", "This is a test message.")

    # Assert the template file was opened correctly
    mock_open_file.assert_called_with("./utils/emails/index.html", "r", encoding="utf-8")
    mock_render.assert_called()

    # Assert that the email send method was called once
    mock_send_email_method.assert_called_once()

    # Verify the response from sendEmail
    assert response.status_code == 200
    assert json.loads(response.body) == {
        "status": 200,
        "message": "Operation was successful",
    }
