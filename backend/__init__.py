from flask import Flask
from .models import db

def create_app():
    app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db.init_app(app)

    from .app import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app
