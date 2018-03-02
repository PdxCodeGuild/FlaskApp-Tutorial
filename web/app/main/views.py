import datetime
import logging
import os

from flask import current_app, escape
from . import main


@main.route('/main/')
def hello_main():
    logging.info("hello_main()")
    return 'Hello FlaskApp : Main Module'


@main.route('/info/date')
def info_date():
    ts = datetime.datetime.now().strftime("%Y/%m/%d @ %H:%M:%S")
    return "Current Datetime : %s" % ts


@main.route('/info/config')
def info_config():
    cnf = dict(current_app.config)
    return "'%s' Config : %s" % (os.getenv('FLASK_CONFIG'),cnf)


@main.route('/info/url_map')
def info_url_map():
    return "current_app.url_map:<pre> %s </pre>" % escape(current_app.url_map)





