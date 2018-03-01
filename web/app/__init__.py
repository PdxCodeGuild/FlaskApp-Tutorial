from flask import Flask
from config import AppConfig

def create_app():
    app = Flask(__name__)

    app.config.from_object(AppConfig)
    AppConfig.init_app(app)

    return app
