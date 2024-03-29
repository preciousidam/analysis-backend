import os
from dotenv import load_dotenv

from pathlib import Path  # python3 only
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    DEBUG = True
    TESTING = True
    APP = os.getenv('FLASK_APP')
    SERVER_PORT = int(os.getenv('SERVER_PORT'))
    SECRET_KEY = os.getenv('SECRET_KEY')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = bool(
        os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'))
    SQLALCHEMY_ENGINE_OPTIONS = {'pool_recycle': int(
        os.getenv('SQLALCHEMY_POOL_RECYCLE', 2000))}

    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_DEBUG = False
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_SUPPRESS_SEND = False
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    FLASK_ADMIN_SWATCH = os.getenv('FLASK_ADMIN_SWATCH')
    CLOUD_NAME = os.getenv('CLOUD_NAME')
    CLOUD_API_KEY = os.getenv('CLOUD_API_KEY')
    CLOUD_API_SECRET = os.getenv('CLOUD_API_SECRET')


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(Path('../'), 'test.db')


class DevelopementConfig(Config):
    ENV = os.getenv('ENV')
    FLASK_ENV = os.getenv('ENV')


class ProductionConfig(Config):
    ENV = os.getenv('ENV')
    FLASK_ENV = os.getenv('ENV')
