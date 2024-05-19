import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)))

class Config:
    SECRET_KEY =os.getenv('SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(minutes=60)
    JWT_REFRESH_TOKEN_EXPIRES=timedelta(minutes=60)
    JWT_SECRET_KEY=os.getenv('JWT_SECRET_KEY')

    


class DevConfig(Config):
    DEBUG = os.getenv('DEBUG')
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(BASE_DIR, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS')
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api', 'uploads')

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass

config_dict={
    'dev':DevConfig,
    'test':TestConfig,
    'prod':ProdConfig
}