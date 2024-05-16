import pytest
from unittest.mock import patch, MagicMock
from backend.scheduler import send_weekly_event_emails, send_notifications

@patch('backend.scheduler.send_email')
def test_send_weekly_event_emails(mock_send_email):
    send_weekly_event_emails()
    assert mock_send_email.called

@patch('backend.scheduler.send_email')
def test_send_notifications(mock_send_email):
    send_notifications()
    assert mock_send_email.called
