from flask import jsonify
from .. import db
from ..item.models import ItemModel
from . import api


@api.route('/item/')
def get_items():
    rows = db.session.query(ItemModel)
    return jsonify({ 'item': [item.to_json() for item in rows] })

@api.route('/item/<int:id>/')
def get_item(id):
    item = ItemModel.query.get_or_404(id)
    return jsonify(item.to_json())
