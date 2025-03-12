#config.py
import os

class Config:

    SQLALCHEMY_TRACK_MODIFICATIONS = True
    
    GIT_REPO_PATH = os.getenv("GIT_REPO_PATH")
    GIT_REPO_BRANCH = os.getenv("GIT_REPO_BRANCH")
    GIT_REPO_SECRET = os.getenv("GIT_REPO_SECRET")

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")
    SECRET_KEY = os.getenv("DEV_SECRET_KEY")
    SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TST_DATABASE_URL")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("PROD_DATABASE_URL")

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}