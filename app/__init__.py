import os

from flask import Flask
from .extensions import api, db
from .resources import ns

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    # postgresql://desafio_782f_user:HetMfgdmmDQXXxfQIE2Bd589FxElotNm@dpg-cne1bsun7f5s73bnj080-a.oregon-postgres.render.com/desafio_782f

    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)

    return app