from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, static_folder="../frontend/", static_url_path="/")
    app.config.from_object('backend.config.Config')
    db.init_app(app)
    CORS(app)

    with app.app_context():
        from .models import Event, Notification
        db.create_all()

    from .app import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
