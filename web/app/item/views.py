import logging
import math

from flask import abort, current_app, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required
from jinja2 import TemplateNotFound
from .. import config_default as CONFIG
from .. import db, flash_errors
from ..decorators import get_list_opts, role_required
from ..user.models import UserModel
from . import item
from .models import ItemModel, ItemUserModel, get_owner_id_choices
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
@role_required(CONFIG.USER_ROLE_EDIT)
def item_action():
    action   = request.values.get('action', '')
    item_ids = request.form.getlist('item_id')
    id_str = "["+",".join([str(id) for id in item_ids])+"]"

    if action and item_ids:
        if action == 'delete':
            for id in item_ids:
                item_delete( id )
        if action in ['approved','completed','draft','hidden']:
            new_status = current_app.config['ITEM_STATUS_APPROVED']
            if action == 'completed':
                new_status = current_app.config['ITEM_STATUS_COMPLETED']
            elif action == 'draft':
                new_status = current_app.config['ITEM_STATUS_DRAFT']
            elif action == 'hidden':
                new_status = current_app.config['ITEM_STATUS_HIDDEN']
            for id in item_ids:
                item = ItemModel.query.get_or_404(id)
                if item.item_status != new_status:
                    item.item_status = new_status
                    db.session.add(item)
            db.session.commit()
            flash("Items Set %s (id=%s)" % (current_app.config['ITEM_STATUS'][new_status],id_str),'success')
    logging.info('item_action - action:%s, item_ids:%s' % (action, id_str))
    return redirect(url_for('.item_list'))


@item.route('/admin/item/delete/<int:id>', methods=['GET','POST'])
@role_required(CONFIG.USER_ROLE_EDIT)
def item_delete( id ):
    item = ItemModel.query.get_or_404(id)
    if current_user.id == item.owner_id or current_user.user_role == current_app.config['USER_ROLE_ADMIN']:
        db.session.delete(item)
        db.session.commit()
        flash('Item Deleted (id=%s)' % (item.id),'success')
        logging.info('item_delete( id:%s )' % (item.id))
    else:
        flash('Permission Denied - Item Not Deleted ( id:%s )' % (item.id))
    return redirect(url_for('.item_list'))


@item.route('/admin/item/create', methods=['GET','POST'])
@role_required(CONFIG.USER_ROLE_EDIT)
def item_create():
    item = ItemModel()
    form = CreatItemForm(item)
    if form.validate_on_submit():
        form.populate_obj(item)
        item.owner_id = current_user.id
        db.session.add(item)
        db.session.commit()
        flash('Item Created (id=%s)' % (item.id),'success')
        logging.info('item_create( id:%s )' % (item.id))
        return redirect(url_for('.item_view', id=item.id))
    else:
        flash_errors(form)
    if request.method == 'GET':
        item.keyname = ''
        form.process(obj=item)
    return render_template('item_create.html', form=form)


@item.route('/admin/item/edit/<int:id>', methods=['GET','POST'])
@role_required(CONFIG.USER_ROLE_EDIT)
def item_edit( id ):
    item = ItemModel.query.get_or_404(id)
    form = EditItemForm(item)
    form.owner_id.choices = get_owner_id_choices()
    form.users_id.choices = get_owner_id_choices()
    if form.validate_on_submit():
        del form.mod_create, form.mod_update

        # convert user_id data to ItemUserModel objects
        # delete previous relations not in current selection
        item_users = ItemUserModel.query.filter_by(item_id=id).all()
        for item_user in item_users:
            if not item_user.user_id in form.users_id.data:
                logging.debug('1- item_edit( delete:%s )' % (item_user))
                db.session.delete(item_user)
                db.session.commit()
        # insert/update current relations
        for user_id in form.users_id.data:
            item_user = ItemUserModel.query.filter_by(item_id=id,user_id=user_id).first()
            if not item_user:
                item_user = ItemUserModel(item_id=id,user_id=user_id,relation='editor')
                logging.debug('2- item_edit( insert:%s )' % (item_user))
                db.session.add(item_user)
            elif item_user.relation != 'editor':
                item_user.relation = 'editor'
                logging.debug('3- item_edit( update:%s )' % (item_user))
                db.session.add(item_user)
        # remove form.users_id prior to populate_obj(item)
        del form.users_id

        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()
        flash('Item Updated (id=%s)' % (item.id),'success')
        logging.info('item_edit( id:%s )' % (item.id))
        return redirect(url_for('.item_view', id=item.id))
    else:
        flash_errors(form)
    form.process(obj=item)
    return render_template('item_edit.html', form=form)


@item.route('/admin/item/view/<int:id>')
@role_required(CONFIG.USER_ROLE_EDIT)
def item_view( id ):
    item = ItemModel.query.get_or_404(id)
    cols = ItemModel.__table__.columns.keys()
    return render_template('item_view.html', cols=cols, item=item)


@item.route('/admin/item/list', methods=['GET','POST'])
@get_list_opts('item_list_opts')
@role_required(CONFIG.USER_ROLE_EDIT)
def item_list():
    cols = ItemModel.__table__.columns.keys()
    cols_filtered = list(filter(lambda x: x not in ['item_text'], cols))
    rows = db.session.query(ItemModel)

    opts_key = 'item_list_opts'
    S = session[opts_key]

    if S['item_status'] >= current_app.config['ITEM_STATUS_HIDDEN']:
        rows = rows.filter(ItemModel.item_status == S['item_status'])

    S['itemcnt'] = rows.count()
    S['pagecnt'] = int(math.ceil( float(S['itemcnt'])/float(S['limit']) ))

    if S['page'] > S['pagecnt']:
        S['page'] = S['pagecnt']
    S['offset'] = 0
    if ((S['page'] - 1) * S['limit']) < S['itemcnt']:
        S['offset'] = (S['page'] - 1) * S['limit']
    session[opts_key] = S

    if S['sort'] == 'owner_id':
        rows = rows.outerjoin(UserModel)
        #rows = rows.options( db.joinedload(ItemModel.owner_id).load_only("keyname", "user_email") )
        rows = rows.options( \
            db.Load(ItemModel).defer("item_text"), \
            db.Load(UserModel).load_only("keyname", "user_email"), \
        )

        if S['order'] == 'desc':
            rows = rows.order_by(getattr( UserModel, 'keyname' ).desc())
        else:
            rows = rows.order_by(getattr( UserModel, 'keyname' ).asc())
    elif S['sort'] in cols_filtered:
        if S['order'] == 'desc':
            rows = rows.order_by(getattr( ItemModel, S['sort'] ).desc())
        else:
            rows = rows.order_by(getattr( ItemModel, S['sort'] ).asc())
    if S['offset'] > 0:
        rows = rows.offset(S['offset'])
    if S['limit'] > 0:
        rows = rows.limit(S['limit'])

    rowcnt = rows.count()
    logging.debug('item_list - %s' % (rowcnt))
    return render_template('item_list.html', cols=cols_filtered,rows=rows,rowcnt=rowcnt,opts_key=opts_key)


@item.route('/hello_orm')
def hello_orm():

    rows = db.session.query(ItemModel)
    #rows = rows.filter(ItemModel.id == 1000)

    #from ..user.models import UserModel
    #rows = rows.join(UserModel)
    #rows = rows.order_by(getattr( UserModel, 'keyname' ).asc())
    #rows = rows.filter(UserModel.id == 1000)

    #rows = rows.join('owner')
    rows = rows.outerjoin('owner')
    rows = rows.order_by("item.owner_id IS NULL, user.keyname ASC")
    #rows = rows.filter("user.id = 1000")

    i = 0
    cols_item = None
    cols_user = None
    result = '<b>db.session.query(ItemModel)</b>'
    for row in rows:
        if cols_item == None and row.__table__.columns:
            cols_item  = row.__table__.columns.keys()
        if cols_user == None and row.owner.__table__.columns:
            cols_user  = row.owner.__table__.columns.keys()
        if i == 0:
            result += '<br/>| '
            for col in cols_item:
                result += '<b>item.'+str(col)+'</b> | '
            for col in cols_user:
                result += '<b>user.'+str(col)+'</b> | '

        result += '<br/>| '
        for col in cols_item:
            result += '%s | ' % getattr( row, col )
        for col in cols_user:
            result += '%s | ' % getattr( row.owner, col ) if row.owner else 'None | '

        i += 1

    return result


@item.route('/hello_item_users')
def hello_item_users():
    rows = db.session.query(ItemModel)

    result = '<b>db.session.query(ItemModel)</b>'
    for row in rows:
        result += '<br/>| %s | ' % (row)
        for iu in row.item_users:
            result += ' %s | ' % (iu.user)
    return result
