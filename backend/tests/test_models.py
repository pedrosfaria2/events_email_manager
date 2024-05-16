import pytest
from backend.models import Event, Notification

def test_event_model(init_db):
    event = Event(
        title='Test Event', 
        description='This is a test event', 
        date='2024-12-31',
        start_time='10:00',
        end_time='11:00',
        recurrence=1,
        all_day=False
    )
    init_db.session.add(event)
    init_db.session.commit()

    assert event in init_db.session

def test_notification_model(init_db):
    notification = Notification(
        subject='Test Notification', 
        message='This is a test notification'
    )
    init_db.session.add(notification)
    init_db.session.commit()

    assert notification in init_db.session
