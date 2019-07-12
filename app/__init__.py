
from flask_api import FlaskAPI

from instance.config import app_config

from app.blueprints import main_route

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.register_blueprint(main_route)
    return app


