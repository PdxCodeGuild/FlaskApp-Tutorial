
from flask import Flask
from config import config

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    init_logging(app)

    return app

def init_logging(app):
    import logging
    logging.basicConfig( filename = app.config['LOG_FILE'], level = app.config['LOG_LEVEL'] )
    logging.debug("init_logging( filename = %s, level = %i )" % (app.config['LOG_FILE'],app.config['LOG_LEVEL']))
