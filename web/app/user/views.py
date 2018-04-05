import logging
import math

from flask import abort, current_app, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from jinja2 import TemplateNotFound
from .. import db, flash_errors
from . import user
from .models import UserModel
from .forms import CreatUserForm, EditUserForm, LoginForm
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


@user.route('/login', methods=['GET','POST'])
def user_login():
    user = UserModel()
    form = LoginForm(user)
    if form.validate_on_submit():
        user = UserModel.query.filter_by(user_email=form.user_email.data).first()
        if user is not None and user.user_pass is None:
            user.password = form.password.data
        if user is not None and user.verify_password(form.password.data):
            user.update_mod_login()
            login_user(user, form.remember.data)
            return redirect(form.next.data or url_for('main.main_home'))
        flash('Invalid username or password','warning')
    else:
        flash_errors(form)
    form.next.data = request.args.get('next') or url_for('main.main_home')
    return render_template('user_login.html', form=form)


@user.route('/logout')
#@login_required
def user_logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.main_page', page='index'))


@user.route('/profile')
@login_required
def user_profile():
    cols = UserModel.__table__.columns.keys()
    cols_filtered = list(filter(lambda x: x not in ['id','user_pass'], cols))
    user = UserModel.query.get_or_404( current_user.id )
    return render_template('user_profile.html', cols=cols_filtered, user=user)


@user.route('/admin/user/action', methods=['POST'])
@login_required
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
                if user.user_role == current_app.config['USER_ROLE_NONE']:
                    user.user_role = current_app.config['USER_ROLE_VIEW']
                    db.session.add(user)
            db.session.commit()
            flash('Users Activated (id='+id_str+')')
        if action == 'inactive':
            for id in user_ids:
                user = UserModel.query.get_or_404(id)
                user.user_role = current_app.config['USER_ROLE_NONE']
                db.session.add(user)
            db.session.commit()
            flash('Users Deactivated (id='+id_str+')')
    logging.info('user_action - action:%s, user_ids:%s' % (action, id_str))
    return redirect(url_for('.user_list'))


@user.route('/admin/user/delete/<int:id>', methods=['GET','POST'])
@login_required
def user_delete( id ):
    user = UserModel.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted (id=%s)' % (user.id))
    logging.info('user_delete( id:%s )' % (user.id))
    return redirect(url_for('.user_list'))


@user.route('/admin/user/create', methods=['GET','POST'])
@login_required
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
@login_required
def user_edit( id ):
    user = UserModel.query.get_or_404(id)
    form = EditUserForm(user)
    if form.validate_on_submit():
        del form.cnt_login, form.mod_login, form.mod_create, form.mod_update
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
@login_required
def user_view( id ):
    cols = UserModel.__table__.columns.keys()
    user = UserModel.query.get_or_404(id)
    return render_template('user_view.html', cols=cols, user=user)


@user.route('/admin/user/list', methods=['GET','POST'])
@get_list_opts('user_list_opts')
@login_required
def user_list():
    cols = UserModel.__table__.columns.keys()
    cols_filtered = list(filter(lambda x: x not in ['user_pass'], cols))
    rows = db.session.query(UserModel)

    opts_key = 'user_list_opts'
    S = session[opts_key]

    if S['user_role'] == current_app.config['USER_ROLE_NONE']:
        rows = rows.filter(UserModel.user_role == S['user_role'])
    elif S['user_role'] >= current_app.config['USER_ROLE_VIEW']:
        rows = rows.filter(UserModel.user_role >= S['user_role'])

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

    rowcnt = rows.count()
    logging.debug('user_list - %s' % (rowcnt))
    return render_template('user_list.html', cols=cols_filtered,rows=rows,rowcnt=rowcnt,opts_key=opts_key)


@user.route('/hello_user_items')
def hello_user_items():
    rows = db.session.query(UserModel)

    result = '<b>db.session.query(UserModel)</b>'
    for row in rows:
        result += '<br/>| %s | ' % (row)
        for iu in row.user_items:
            result += " %s | " % (iu.item)
    return result
