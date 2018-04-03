from flask import g
from flask_httpauth import HTTPBasicAuth
from ..user.models import UserModel
from . import api
from .errors import forbidden, unauthorized

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(email,password):
    if not email:
        return False
    user = UserModel.query.filter_by(user_email=email).first()
    if not user:
        return False
    g.current_user = user
    return user.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid Credentials')


@api.before_request
@auth.login_required
def before_request():
    if not g.current_user.active:
        return forbidden('Inactive Account')


