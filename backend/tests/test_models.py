from datetime import datetime
from backend.models import Event, Notification, db

def test_event_model(init_db):
    event = Event(
        title='Test Event',
        description='This is a test event',
        date=datetime.strptime('2024-12-31', '%Y-%m-%d').date(),
        start_time='10:00',
        end_time='11:00',
        tags='meeting, client'
    )
    db.session.add(event)
    db.session.commit()
    assert event.id is not None

def test_notification_model(init_db):
    notification = Notification(
        subject='Test Notification',
        message='This is a test notification'
    )
    db.session.add(notification)
    db.session.commit()
    assert notification.id is not None
