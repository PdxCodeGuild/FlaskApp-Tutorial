from flask import g, jsonify
from .. import db
from ..item.models import ItemModel
from ..user.models import UserModel
from . import api


@api.route('/user/')
def get_profile():
    user = UserModel.query.get_or_404( g.current_user.id )
    return jsonify({ 'user': [user.to_json()] })

@api.route('/user/count/')
def get_user_count():
    cnt = db.session.query(UserModel).count()
    return jsonify({ 'user': cnt })

@api.route('/user/list/')
def get_user_list():
    rows = db.session.query(UserModel)
    return jsonify({ 'user': [user.to_json() for user in rows] })

@api.route('/user/<int:id>/')
def get_user(id):
    user = UserModel.query.get_or_404(id)
    return jsonify({ 'user': [user.to_json()] })

@api.route('/user/<int:id>/item/')
@api.route('/user/<int:id>/item/owner/')
def get_user_item_owner(id):
    user = UserModel.query.get_or_404(id)
    return jsonify({ 'item': [item.to_json() for item in user.items] })

@api.route('/user/<int:id>/item/editor/')
def get_user_item_editor(id):
    user = UserModel.query.get_or_404(id)
    return jsonify({ 'item': [iu.item.to_json() for iu in user.user_items] })

