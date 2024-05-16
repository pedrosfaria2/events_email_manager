class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///monitoring_app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TESTING = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_monitoring_app.db'
    TESTING = True
