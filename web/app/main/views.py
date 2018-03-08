import datetime
import logging
import os

from flask import abort, current_app, escape, redirect, render_template, url_for
from jinja2 import TemplateNotFound
from . import main


@main.route('/home/')
def main_home():
    return redirect(url_for('.main_page'))


@main.route('/', defaults={'page': 'index'})
@main.route('/<page>/')
def main_page(page):
    try:
        logging.debug( "main_page( %s )" % page )
        title = "FlaskApp Page"
        return render_template('%s.html' % (page), page_title=title)
    except TemplateNotFound:
        logging.info('TemplateNotFound: %s.html' % (page))
        abort(404)


@main.route('/info/')
def main_info():
    result = ''
    result += '<br/><a href="'+url_for('.info_date')+'">show datetime</a>'
    result += '<br/><a href="'+url_for('.info_config')+'">show app.config</a>'
    result += '<br/><a href="'+url_for('.info_url_map')+'">show url_map</a>'
    return result


@main.route('/info/date')
def info_date():
    ts = datetime.datetime.now().strftime("%Y/%m/%d @ %H:%M:%S")
    return "Current Datetime :<pre> %s </pre>" % ts


@main.route('/info/config')
def info_config():
    cnf = dict(current_app.config)
    return "'%s' Config :<pre> %s </pre>" % (os.getenv('FLASK_CONFIG'),cnf)


@main.route('/info/url_map')
def info_url_map():
    return "current_app.url_map :<pre> %s </pre>" % escape(current_app.url_map)


