from flask import Flask, flash
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
config_default = config['default']

def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    init_logging(app)

    bootstrap.init_app(app)
    db.init_app(app)

    init_login_manager(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .item import item as item_blueprint
    app.register_blueprint(item_blueprint)

    from .user import user as user_blueprint
    app.register_blueprint(user_blueprint)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

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

def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.session_protection = 'strong'
    login_manager.login_view = 'user.user_login'
    login_manager.login_message = u"Please log in to access this page."
    login_manager.login_message_category = "warning"
    login_manager.refresh_view = 'user.user_login'
    login_manager.needs_refresh_message = (u"Please confirm your credentials to access this page.")
    login_manager.needs_refresh_message_category = "warning"
