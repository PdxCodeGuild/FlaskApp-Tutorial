import logging
import math

from flask import flash, redirect, render_template, request, session, url_for
from jinja2 import TemplateNotFound
from .. import db, flash_errors
from . import user
from .models import UserModel
from .forms import CreatUserForm, EditUserForm
from ..decorators import get_list_opts


@user.route('/user/', defaults={'page': 'index'})
@user.route('/user/<page>/')
def user_page(page):
    try:
        logging.debug( 'user_page( page:%s )' % (page) )
        return render_template('user_%s.html' % (page))
    except TemplateNotFound:
        logging.info('TemplateNotFound: user_%s.html' % (page))
        abort(404)


@user.route('/admin/user/action', methods=['POST'])
def user_action():
    action   = request.values.get('action', '')
    user_ids = request.form.getlist('user_id')
    id_str = "["+",".join([str(id) for id in user_ids])+"]"

    if action and user_ids:
        if action == 'delete':
            for id in user_ids:
                user = UserModel.query.get_or_404(id)
                db.session.delete(user)
            db.session.commit()
            flash('Users Deleted (id='+id_str+')')
        if action == 'active':
            for id in user_ids:
                user = UserModel.query.get_or_404(id)
                user.active = True
                db.session.add(user)
            db.session.commit()
            flash('Users Activated (id='+id_str+')')
        if action == 'inactive':
            for id in user_ids:
                user = UserModel.query.get_or_404(id)
                user.active = False
                db.session.add(user)
            db.session.commit()
            flash('Users Deactivated (id='+id_str+')')
    logging.info('user_action - action:%s, user_ids:%s' % (action, id_str))
    return redirect(url_for('.user_list'))


@user.route('/admin/user/delete/<int:id>', methods=['GET','POST'])
def user_delete( id ):
    user = UserModel.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted (id=%s)' % (user.id))
    logging.info('user_delete( id:%s )' % (user.id))
    return redirect(url_for('.user_list'))


@user.route('/admin/user/create', methods=['GET','POST'])
def user_create():
    user = UserModel()
    form = CreatUserForm(user)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('User created (id=%s)' % (user.id))
        logging.info('user_create( id:%s )' % (user.id))
        return redirect(url_for('.user_view', id=user.id))
    else:
        flash_errors(form)
    if request.method == 'GET':
        user.keyname = ''
        form.process(obj=user)
    return render_template('user_create.html', form=form)


@user.route('/admin/user/edit/<int:id>', methods=['GET','POST'])
def user_edit( id ):
    user = UserModel.query.get_or_404(id)
    form = EditUserForm(user)
    if form.validate_on_submit():
        if form.password.data == '':
            del form.password
        form.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        flash('User updated (id=%s)' % (user.id))
        logging.info('user_edit( id:%s )' % (user.id))
        return redirect(url_for('.user_view', id=user.id))
    else:
        flash_errors(form)
    form.process(obj=user)
    return render_template('user_edit.html', form=form)


@user.route('/admin/user/view/<int:id>')
def user_view( id ):
    cols = UserModel.__table__.columns.keys()
    user = UserModel.query.get_or_404(id)
    return render_template('user_view.html', cols=cols, user=user)


@user.route('/admin/user/list', methods=['GET','POST'])
@get_list_opts('user_list_opts')
def user_list():
    cols = UserModel.__table__.columns.keys()
    cols_filtered = list(filter(lambda x: x not in ['user_pass'], cols))
    rows = db.session.query(UserModel)

    opts_key = 'user_list_opts'
    S = session[opts_key]

    if S['status'] in ['active', 'inactive']:
        rows = rows.filter(UserModel.active == (S['status'] == 'active'))

    S['itemcnt'] = rows.count()
    S['pagecnt'] = int(math.ceil( float(S['itemcnt'])/float(S['limit']) ))

    if S['page'] > S['pagecnt']:
        S['page'] = S['pagecnt']
    S['offset'] = 0
    if ((S['page'] - 1) * S['limit']) < S['itemcnt']:
        S['offset'] = (S['page'] - 1) * S['limit']
    session[opts_key] = S

    if S['sort'] in cols:
        if S['order'] == 'desc':
            rows = rows.order_by(getattr( UserModel, S['sort'] ).desc())
        else:
            rows = rows.order_by(getattr( UserModel, S['sort'] ).asc())
    if S['offset'] > 0:
        rows = rows.offset(S['offset'])
    if S['limit'] > 0:
        rows = rows.limit(S['limit'])

    rows = rows.all()
    rowcnt = len(rows)

    logging.debug('user_list - %s' % (rowcnt))
    return render_template('user_list.html', cols=cols_filtered,rows=rows,rowcnt=rowcnt,opts_key=opts_key)


