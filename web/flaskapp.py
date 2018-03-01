
# call create_app() in app/__init__.py
from app import create_app
app = create_app()


@app.route('/')
def hello_flaskapp():
    return 'Hello FlaskApp'


# run 'docker ps' to get the flaskapp_web CONTAINER_ID
# run 'docker attach CONTAINER_ID' to connect a terminal session
# pdb.set_trace() will launch the debugger in the attached terminal
# see https://docs.python.org/3.6/library/pdb.html?highlight=pdb#debugger-commands
@app.route('/debug')
def hello_debug():
    import pdb; pdb.set_trace()
    return "Hello Python Debugger"


@app.route('/info/date')
def info_date():
    import datetime
    ts = datetime.datetime.now().strftime("%Y/%m/%d @ %H:%M:%S")
    return "Current Datetime : %s" % ts


@app.route('/info/config')
def app_config():
    cnf = dict(app.config)
    return "Current Config : %s" % cnf

