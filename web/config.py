# see http://flask.pocoo.org/docs/0.12/api/

import os

class AppConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kp-cUHRAYH1n-sPaJICcEE2kOpU62mCk'

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(AppConfig):
    DEBUG = True

class TestingConfig(AppConfig):
    TESTING = True


class ProductionConfig(AppConfig):
    DEBUG = False
    TESTING = False

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
