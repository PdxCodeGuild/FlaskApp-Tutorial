import logging

from flask import current_app, escape
from . import item


@item.route('/item/')
def hello_item():
    logging.info("hello_item()")
    return 'Hello FlaskApp : Item Module'
