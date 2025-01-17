#config.py
import os

class Config:

    GIT_REPO_PATH = os.getenv("GIT_REPO_PATH")
    GIT_REPO_BRANCH = os.getenv("GIT_REPO_BRANCH")
    GIT_REPO_SECRET = os.getenv("GIT_REPO_SECRET")

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

class ProductionConfig(Config):
    pass

config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig
}