from backend import create_app, db
from backend.models import Event, Notification

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
