from flask import jsonify
from .. import db
from ..user.models import UserModel
from . import api


@api.route('/user/')
def get_users():
    rows = db.session.query(UserModel)
    return jsonify({ 'user': [user.to_json() for user in rows] })

@api.route('/user/<int:id>/')
def get_user(id):
    user = UserModel.query.get_or_404(id)
    return jsonify(user.to_json())
