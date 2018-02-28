from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_flaskapp():
    return 'Hello FlaskApp'

@app.route('/info/date')
def info_date():
    import datetime
    ts = datetime.datetime.now().strftime("%Y/%m/%d @ %H:%M:%S")

    return "Current Datetime : %s" % ts
