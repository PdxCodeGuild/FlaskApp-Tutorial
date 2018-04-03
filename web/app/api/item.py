from flask import g, jsonify
from .. import db
from ..item.models import ItemModel
from ..user.models import UserModel
from . import api


@api.route('/item/')
def get_profile_items():
    user = UserModel.query.get_or_404( g.current_user.id )
    return jsonify({ 'item': [item.to_json() for item in user.items] })

@api.route('/item/count/')
def get_item_count():
    cnt = db.session.query(ItemModel).count()
    return jsonify({ 'item': cnt })

@api.route('/item/list/')
def get_item_list():
    rows = db.session.query(ItemModel)
    return jsonify({ 'item': [item.to_json() for item in rows] })

@api.route('/item/<int:id>/')
def get_item(id):
    item = ItemModel.query.get_or_404(id)
    return jsonify({ 'item': [item.to_json()] })

@api.route('/item/<int:id>/owner/')
def get_item_owner(id):
    item = ItemModel.query.get_or_404(id)
    #return jsonify(item.owner.to_json())
    return jsonify({ 'user': [item.owner.to_json()] })

@api.route('/item/<int:id>/editor/')
def get_item_editor(id):
    item = ItemModel.query.get_or_404(id)
    return jsonify({ 'user': [iu.user.to_json() for iu in item.item_users] })

