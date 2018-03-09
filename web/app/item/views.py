import logging

from flask import render_template
from .. import db
from . import item

from .models import ItemModel


@item.route('/item/')
def hello_item():
    logging.info("hello_item()")
    return 'Hello FlaskApp : Item Module'


@item.route('/admin/item/delete/<int:id>')
def item_delete( id ):
    return 'item_delete - id:%s' % (id)

@item.route('/admin/item/create')
def item_create():
    return 'item_create'

@item.route('/admin/item/edit/<int:id>')
def item_edit( id ):
    return 'item_edit - id:%s' % (id)


@item.route('/admin/item/view/<int:id>')
def item_view( id ):
    item = ItemModel.query.get_or_404(id)
    cols = ItemModel.__table__.columns.keys()
    return render_template('item_view.html', cols=cols, item=item)


@item.route('/admin/item/list')
def item_list():
    cols = ItemModel.__table__.columns.keys()

    rows = db.session.query(ItemModel)
    rows = rows.order_by(getattr( ItemModel, 'id' ).asc())
    rows = rows.all()

    rowcnt = len(rows)

    logging.debug('item_list - %s' % (rowcnt))
    return render_template('item_list.html', cols=cols,rows=rows,rowcnt=rowcnt)


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
