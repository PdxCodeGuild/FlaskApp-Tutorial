import logging

from .. import db
from . import item

from .models import ItemModel


@item.route('/item/')
def hello_item():
    logging.info("hello_item()")
    return 'Hello FlaskApp : Item Module'


@item.route('/hello_orm')
def hello_orm():
    cols  = ItemModel.__table__.columns.keys()
    rows = db.session.query(ItemModel)

    result = '<b>db.session.query(ItemModel)</b>'
    result += '<br/>| '
    for col in cols:
        result += '<b>'+str(col)+'</b> | '
    for row in rows:
        result += '<br/>| '
        for col in cols:
            result += '%s | ' % getattr( row, col )
    return result


