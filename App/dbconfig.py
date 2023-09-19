#config.py
import os

class dbConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

    class DevelopmentConfig(dbConfig):
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL")

    dbConfig = {
    "development": DevelopmentConfig,
    }