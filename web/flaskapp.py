import datetime
import logging
import os

from flask import flash, render_template
from markupsafe import Markup

# call create_app() in app/__init__.py
from app import create_app
app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.route('/hello_flaskapp')
def hello_flaskapp():
    title = "Hello FlaskApp"
    logging.info("hello_flaskapp() : %s" % title)
    flash(Markup("hello_flaskapp() : %s" % title), 'success')
    return render_template('hello.html', page_title=title)


# run 'docker ps' to get the flaskapp_web CONTAINER_ID
# run 'docker attach CONTAINER_ID' to connect a terminal session
# pdb.set_trace() will launch the debugger in the attached terminal
# see https://docs.python.org/3.6/library/pdb.html?highlight=pdb#debugger-commands
@app.route('/hello_debug')
def hello_debug():
    import pdb; pdb.set_trace()
    logging.info("hello_debug()")
    return "Hello Python Debugger"


# Forbidden Page
@app.errorhandler(403)
def page_restricted(e):
    return render_template('403.html', error=e), 403

# Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', error=e), 404

# Deleted Page
@app.errorhandler(410)
def page_deleted(e):
    return render_template('410.html', error=e), 410
