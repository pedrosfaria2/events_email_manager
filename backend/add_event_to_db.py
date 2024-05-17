from datetime import datetime
from backend.models import db, Event

def add_events_to_db(events):
    for event in events:
        event_date = datetime.strptime(event["date"], '%Y-%m-%d').date()
        new_event = Event(
            title=event["title"],
            description=event["description"],
            date=event_date,
            start_time=event["start_time"],
            end_time=event["end_time"],
            tags=event["tags"]
        )
        db.session.add(new_event)
    db.session.commit()
