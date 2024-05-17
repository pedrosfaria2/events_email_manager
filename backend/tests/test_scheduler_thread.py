import pytest
from unittest.mock import patch, MagicMock
from backend import create_app
from backend.scheduler_thread import send_weekly_automatic_exercise_email, send_notifications, start_scheduler_thread
from datetime import datetime

@pytest.fixture
def app():
    app = create_app(config_name='testing')
    with app.app_context():
        yield app

def test_send_weekly_automatic_exercise_email(app):
    with patch('backend.scheduler_thread.send_email') as mock_send_email:
        mock_event = MagicMock()
        mock_event.title = "Test Event"
        mock_event.date = datetime(2024, 5, 17)
        mock_event.description = "Test Description"
        mock_event.tags = "automatic exercise"

        with patch('backend.scheduler_thread.Event.query.filter') as mock_filter:
            mock_filter.return_value.all.return_value = [mock_event]

            send_weekly_automatic_exercise_email(app)

            mock_send_email.assert_called_once_with(
                "Upcoming Automatic Exercise Events at B3",
                "Dear customer,\n\nWe would like to inform you about the following automatic exercises at B3 this week:\n\n>>> Test Event on 2024-05-17\n\n      Test Description\n\n\n\nBest regards and good trading,\nHFT Team of Nova Futura Investimentos.",
                "pedro.faria@novafutura.com.br"
            )

def test_start_scheduler_thread(app):
    with patch('backend.scheduler_thread.schedule') as mock_schedule:
        start_scheduler_thread(app)

        mock_schedule.every.return_value.friday.at.assert_called_once_with("15:30")
        mock_schedule.every.return_value.friday.at.return_value.do.assert_called_once()
