import os
from . import create_app
from .models import gleba
from flask import abort, jsonify

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.route("/gleba/list", methods=["GET"])
def get_gleba():
    gleba = gleba.Gleba.query.all()
    return jsonify([gleba.to_json() for gleba in gleba])

@app.route("/gleba/<int:isbn>", methods=["GET"])
def get_gleba(isbn):
    gleba = gleba.Gleba.query.get(isbn)
    if gleba is None:
        abort(404)
    return jsonify(gleba.to_json())