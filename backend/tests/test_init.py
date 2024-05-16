def test_create_app():
    from backend import create_app

    app = create_app()

    assert app is not None
    assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///app.db'
    assert not app.config['TESTING']

def test_app_context(app):
    with app.app_context():
        from backend.models import db
        assert db is not None
        assert db.engine is not None

def test_app_blueprints(app):
    assert 'main' in app.blueprints
