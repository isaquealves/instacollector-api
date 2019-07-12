
from flask_api import FlaskAPI

from instance.config import app_config

from app.blueprints import main_route, profile_dl, single_post_dl

def create_app(config_name):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    app.register_blueprint(main_route)
    app.register_blueprint(profile_dl)
    app.register_blueprint(single_post_dl)
    return app


