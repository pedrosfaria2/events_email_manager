import pytest
from unittest.mock import patch, MagicMock
from backend.email_service import send_email

@patch('backend.email_service.win32com.client.Dispatch')
def test_send_email(mock_dispatch):
    mock_outlook = MagicMock()
    mock_dispatch.return_value = mock_outlook
    mock_mail = MagicMock()
    mock_outlook.CreateItem.return_value = mock_mail
    
    send_email("Test Subject", "Test Body", "test@example.com")
    
    mock_outlook.CreateItem.assert_called_once_with(0)
    mock_mail.To = "test@example.com"
    mock_mail.Subject = "Test Subject"
    mock_mail.Body = "Test Body"
    mock_mail.Send.assert_called_once()
