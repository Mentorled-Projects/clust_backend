import pytest
from api.utils.email_utils import send_email_reminder
from unittest.mock import patch, MagicMock

@patch("smtplib.SMTP")
def test_send_email_reminder_success(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server

    send_email_reminder("test@example.com", "Test Subject", "Test Content")

    mock_smtp.assert_called_once()
    mock_server.starttls.assert_called_once()
    mock_server.login.assert_called_once()
    mock_server.send_message.assert_called_once()

@patch("smtplib.SMTP")
def test_send_email_reminder_failure(mock_smtp):
    mock_server = MagicMock()
    mock_smtp.return_value.__enter__.return_value = mock_server
    mock_server.login.side_effect = Exception("Login failed")

    with pytest.raises(Exception) as excinfo:
        send_email_reminder("test@example.com", "Test Subject", "Test Content")

    assert "Login failed" in str(excinfo.value)
