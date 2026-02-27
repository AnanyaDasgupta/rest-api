import logging

from dotenv import load_dotenv
from flask import Flask

from app.config import Config
from app.extensions import db
from app.routes import api


def create_app(config_object=Config):
    # Load environment variables from a local .env when present.
    # In production, variables should still be injected by the runtime.
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(config_object)

    logging.basicConfig(
        level=getattr(logging, app.config["LOG_LEVEL"].upper(), logging.INFO),
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
    )

    db.init_app(app)

    api_prefix = f"/api/{app.config['API_VERSION']}"
    app.register_blueprint(api, url_prefix=api_prefix)

    app.logger.info("Configured database backend: %s", app.config["SQLALCHEMY_DATABASE_URI"].split(":", 1)[0])

    return app
