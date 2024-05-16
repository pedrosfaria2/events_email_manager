import pytest
from backend.app import db
from backend.models import Event, Notification
from datetime import datetime

@pytest.fixture
def init_db():
    db.create_all()
    yield db
    db.drop_all()

def test_event_model(app):
    with app.app_context():
        event = Event(title='Test Event', description='This is a test event', date=datetime(2024, 12, 31))
        db.session.add(event)
        db.session.commit()

        assert event in db.session

def test_notification_model(app):
    with app.app_context():
        notification = Notification(subject='Test Notification', message='This is a test notification')
        db.session.add(notification)
        db.session.commit()

        assert notification in db.session
