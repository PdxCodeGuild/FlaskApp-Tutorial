from flask import g, jsonify
from flask_httpauth import HTTPBasicAuth
from ..user.models import UserModel
from . import api
from .errors import forbidden, unauthorized

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(login,password):
    if not login:
        return False
    if not password:
        g.current_user = UserModel.verify_auth_token(login)
        g.token_used = True
        return g.current_user is not None
    user = UserModel.query.filter_by(user_email=login).first()
    if not user:
        return False
    g.current_user = user
    g.token_used = False
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid Credentials')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.user_role:
        return forbidden('Inactive Account')

@api.route('/token')
def get_auth_token():
    if g.token_used:
        return unauthorized('Invalid Credentials')
    return jsonify({'token': g.current_user.generate_auth_token(3600).decode('utf-8'), 'expires': 3600})
