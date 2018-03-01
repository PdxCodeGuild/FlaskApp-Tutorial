# see http://flask.pocoo.org/docs/0.12/api/

import os

class AppConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kp-cUHRAYH1n-sPaJICcEE2kOpU62mCk'

    @staticmethod
    def init_app(app):
        pass
