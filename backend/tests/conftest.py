import sys
import os
import pytest
from backend import create_app, db
from backend.models import Event
from datetime import date

# Adiciona o caminho do backend ao sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

@pytest.fixture
def app():
    app = create_app(config_name='testing')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()

@pytest.fixture
def sample_events():
    return [
        {
            "title": "Event 1",
            "description": "Description for Event 1",
            "date": "2024-05-17",
            "start_time": "08:00",
            "end_time": "19:00",
            "tags": "tag1, tag2"
        },
        {
            "title": "Event 2",
            "description": "Description for Event 2",
            "date": "2024-05-18",
            "start_time": "09:00",
            "end_time": "17:00",
            "tags": "tag3, tag4"
        }
    ]
