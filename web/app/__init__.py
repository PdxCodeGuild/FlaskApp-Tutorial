from flask import Flask, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    init_logging(app)

    bootstrap.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .item import item as item_blueprint
    app.register_blueprint(item_blueprint)

    return app


def init_logging(app):
    import logging
    logging.basicConfig( filename = app.config['LOG_FILE'], level = app.config['LOG_LEVEL'] )
    logging.debug("init_logging( filename = %s, level = %i )" % (app.config['LOG_FILE'],app.config['LOG_LEVEL']))


def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ),'error')
