import logging

from flask import url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db


class UserModel(db.Model):
    __tablename__ = 'user'
    id         = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    active     = db.Column(db.Boolean, nullable=False, index=True, default=1)
    keyname    = db.Column(db.String(63), nullable=False, unique=True, index=True, default='')
    user_email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    user_pass  = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        logging.debug( "password.setter(%s)" %  self.user_email)
        self.user_pass = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_pass, password)

    def to_json(self):
        json_user = {
            #'url': url_for('api.get_user', id=self.id),
            'id'        : self.id,
            'active'    : self.active,
            'keyname'   : self.keyname,
            'user_email': self.user_email,
        }
        return json_user

    def __repr__(self):
        return '<UserModel %r>' % (self.id)
