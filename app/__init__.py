from flask import Flask
from .endpoints.get_value_by_date import get_value_by_date


def create_app():
    app = Flask(__name__)

    # register the endpoints
    app.register_blueprint(get_value_by_date)

    return app
