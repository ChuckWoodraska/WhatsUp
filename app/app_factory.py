from flask import Flask
import configparser
import logging


def create_app(config_path, settings_override=None):
    """
    Create a new app.
    :param config_path:
    :type config_path:
    :param settings_override:
    :type settings_override:
    :return:
    :rtype:
    """
    app = Flask(__name__)
    config = configparser.ConfigParser()
    config.read(config_path)
    # app.config['SERVER_NAME'] = 'localhost'
    app.config["ENVIRONMENT"] = config["ENV"]["STAGE"]

    app.debug = config["ENV"]["STAGE"] == "dev"
    app.secret_key = config["ENV"]["SECRET_KEY"]

    if settings_override:
        app.config.update(settings_override)

    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    from .core import core

    app.register_blueprint(core)


    return app
