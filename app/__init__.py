import logging

from flask import Flask

from app.config import Config
from app.extensions import db
from app.routes import api


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    logging.basicConfig(
        level=getattr(logging, app.config["LOG_LEVEL"].upper(), logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    db.init_app(app)

    api_prefix = f"/api/{app.config['API_VERSION']}"
    app.register_blueprint(api, url_prefix=api_prefix)

    return app
