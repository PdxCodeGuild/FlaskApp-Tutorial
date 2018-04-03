import logging
import os

from flask import current_app, flash, jsonify, render_template, request
from markupsafe import Markup
from app import db

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
# @see https://docs.python.org/3.6/library/pdb.html?highlight=pdb#debugger-commands
@app.route('/hello_debug')
def hello_debug():
    import pdb; pdb.set_trace()
    logging.info("hello_debug()")
    return "Hello Python Debugger"


@app.route('/hello_db')
def hello_db():
    stmt = "SELECT VERSION()"        # Return a string that indicates the MySQL server version
    #stmt = "SELECT CONNECTION_ID()"  # Return the connection ID (thread ID) for the connection
    #stmt = "SELECT CURRENT_USER()"   # The authenticated user name and host name
    #stmt = "SELECT DATABASE()"       # Return the default (current) database name
    stmt = "SHOW TABLES"             # Return list of non-temporary tables in current database

    #stmt = "show create database %s;" % current_app.config['MYSQL_DB']
    #stmt = "show grants for %s;" % current_app.config['MYSQL_USER']

    #stmt = "select * from item"
    #stmt = "select * from user"
    #stmt = "select * from user join item on user.id=item.owner_id"
    #stmt = "select * from item_user"

    #stmt = "SELECT i.id AS item_id, i.keyname, u.id AS user_id, u.keyname FROM item i JOIN item_user iu ON i.id = iu.item_id JOIN user u ON iu.user_id = u.id"
    # users, cnt_items
    #stmt = "SELECT u.keyname, COUNT(i.id) AS cnt_items FROM user u JOIN item_user iu ON u.id = iu.user_id JOIN item i ON i.id = iu.item_id GROUP BY u.keyname"
    # items, cnt_users
    #stmt = "SELECT i.keyname, COUNT(u.id) AS cnt_users FROM item i JOIN item_user iu ON i.id = iu.item_id JOIN user u ON u.id = iu.user_id GROUP BY i.keyname"


    #import pdb; pdb.set_trace()
    eng = db.create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'])
    con = eng.connect()
    rs = con.execute(db.text(stmt))
    con.close()

    cols = rs.keys()
    rows = rs.fetchall()

    result = '<b>'+stmt+'</b>'
    result += '<br/>| '
    for col in cols:
        result += '<b>'+str(col)+'</b> | '
    for row in rows:
        result += '<br/>| '
        for i,col in enumerate(row):
            result += '%s | ' % col
    return result


# Forbidden Page
@app.errorhandler(403)
def page_restricted(e):
    return render_template('403.html', error=e), 403

# Page Not Found
@app.errorhandler(404)
def page_not_found(e):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify({ \
            'code': e.code, 'name': e.name, 'message': e.description, 'url': request.url \
            #, 'error': dir(e), 'request': dir(request) \
            })
        response.status_code = 404
        return response
    return render_template('404.html', error=e), 404

# Deleted Page
@app.errorhandler(410)
def page_deleted(e):
    return render_template('410.html', error=e), 410


# Utility functions available within templates
@app.context_processor
def utility_processor():
    def current_datetime():
        import datetime
        return datetime.datetime.now().strftime("%Y/%m/%d @ %H:%M:%S")
    def debug_queries():
        from flask_sqlalchemy import get_debug_queries
        return get_debug_queries()
    return dict(\
        current_datetime=current_datetime, \
        debug_queries=debug_queries, \
        )
