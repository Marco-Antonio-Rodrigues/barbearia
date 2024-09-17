import logging

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config, ConfigBase

# carrega as variavéis de .env
load_dotenv()

logging.basicConfig(
    format="[%(levelname)s] %(asctime)s %(funcName)s(): %(message)s", level=logging.INFO
)

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    config_object: ConfigBase = Config(config_name)
    app.config.from_object(config_object)
    config_object.init_app()  # pylint: disable=E1101
    db.init_app(app)
    return app
