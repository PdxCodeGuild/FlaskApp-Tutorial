# see http://flask.pocoo.org/docs/0.12/api/

import os
import logging

_basedir = os.path.abspath(os.path.dirname(__file__))

class AppConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kp-cUHRAYH1n-sPaJICcEE2kOpU62mCk'
    LOG_FILE = _basedir+'/logs/flaskapp.log'
    LOG_LEVEL = logging.ERROR  # CRITICAL,ERROR,WARNING,INFO,DEBUG,NOTSET
    BOOTSTRAP_USE_MINIFIED = True
    BOOTSTRAP_SERVE_LOCAL = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(AppConfig):
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class TestingConfig(AppConfig):
    TESTING = True
    LOG_LEVEL = logging.INFO


class ProductionConfig(AppConfig):
    DEBUG = False
    TESTING = False
    LOG_LEVEL = logging.WARNING

    @classmethod
    def init_app(cls, app):
        # multi-step setups could go here
        AppConfig.init_app(app)


config = {
    'development': DevelopmentConfig,
    'testing':     TestingConfig,
    'production':  ProductionConfig,
    'default':     DevelopmentConfig
}
