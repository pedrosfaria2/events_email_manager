import pytest
from unittest.mock import patch, MagicMock
from backend.email_service import send_email

@patch('win32com.client.Dispatch')
def test_send_email(mock_dispatch):
    mock_outlook = MagicMock()
    mock_dispatch.return_value = mock_outlook
    send_email('Test Subject', 'Test Message', 'test@example.com')

    mock_dispatch.assert_called_with('outlook.application')
    assert mock_outlook.CreateItem.called
    mail_item = mock_outlook.CreateItem.return_value
    mail_item.Subject = 'Test Subject'
    mail_item.Body = 'Test Message'
    mail_item.To = 'test@example.com'
    assert mail_item.Send.called
