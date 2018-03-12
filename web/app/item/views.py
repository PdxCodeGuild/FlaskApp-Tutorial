import logging

from flask import flash, redirect, render_template, request, url_for
from jinja2 import TemplateNotFound
from .. import db, flash_errors
from . import item

from .models import ItemModel
from .forms import CreatItemForm, EditItemForm


@item.route('/item/', defaults={'page': 'index'})
@item.route('/item/<page>/')
def item_page(page):
    try:
        logging.debug( 'item_page( page:%s )' % (page) )
        return render_template('item_%s.html' % (page))
    except TemplateNotFound:
        logging.info('TemplateNotFound: item_%s.html' % (page))
        abort(404)


@item.route('/admin/item/action', methods=['POST'])
def item_action():
    action   = request.values.get('action', '')
    item_ids = request.form.getlist('item_id')
    id_str = "["+",".join([str(id) for id in item_ids])+"]"

    if action and item_ids:
        if action == 'delete':
            for id in item_ids:
                item = ItemModel.query.get_or_404(id)
                db.session.delete(item)
            db.session.commit()
            flash('Items Deleted (id='+id_str+')')
        if action == 'active':
            for id in item_ids:
                item = ItemModel.query.get_or_404(id)
                item.active = True
                db.session.add(item)
            db.session.commit()
            flash('Items Activated (id='+id_str+')')
        if action == 'inactive':
            for id in item_ids:
                item = ItemModel.query.get_or_404(id)
                item.active = False
                db.session.add(item)
            db.session.commit()
            flash('Items Deactivated (id='+id_str+')')
    logging.info('item_action - action:%s, item_ids:%s' % (action, id_str))
    return redirect(url_for('.item_list'))


@item.route('/admin/item/delete/<int:id>', methods=['GET','POST'])
def item_delete( id ):
    item = ItemModel.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted (id=%s)' % (item.id))
    logging.info('item_delete( id:%s )' % (item.id))
    return redirect(url_for('.item_list'))


@item.route('/admin/item/create', methods=['GET','POST'])
def item_create():
    item = ItemModel()
    form = CreatItemForm(item)
    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash('Item created (id=%s)' % (item.id))
        logging.info('item_create( id:%s )' % (item.id))
        return redirect(url_for('.item_view', id=item.id))
    else:
        flash_errors(form)
    if request.method == 'GET':
        item.keyname = ''
        form.process(obj=item)
    return render_template('item_create.html', form=form)


@item.route('/admin/item/edit/<int:id>', methods=['GET','POST'])
def item_edit( id ):
    item = ItemModel.query.get_or_404(id)
    form = EditItemForm(item)
    if form.validate_on_submit():
        del form.mod_create, form.mod_update
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash('Item updated (id=%s)' % (item.id))
        logging.info('item_edit( id:%s )' % (item.id))
        return redirect(url_for('.item_view', id=item.id))
    else:
        flash_errors(form)
    form.process(obj=item)
    return render_template('item_edit.html', form=form)


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
