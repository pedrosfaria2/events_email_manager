from flask import Flask, send_from_directory
from .models import db
from .scheduler_thread import start_scheduler_thread

def create_app(config_name='None'):
    app = Flask(__name__, static_folder='../frontend/static', template_folder='../frontend')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_app.db'
        app.config['TESTING'] = True
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    db.init_app(app)

    with app.app_context():
        db.create_all()

    from .app import main as main_blueprint
    from .scheduler_routes import scheduler_bp as scheduler_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(scheduler_blueprint, url_prefix='/api')

    @app.route('/static/<path:path>')
    def static_files(path):
        return send_from_directory(app.static_folder, path)

    start_scheduler_thread(app)

    return app
