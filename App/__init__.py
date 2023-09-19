from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dbconfig import dbconfig

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(dbconfig[config_name])
    dbconfig[config_name].init_app(app)

    db.init_app(app)
    return app