from flask import url_for
from .. import db


class UserModel(db.Model):
    __tablename__ = 'user'
    id         = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    keyname    = db.Column(db.String(63), nullable=False, unique=True, index=True, default='')
    active     = db.Column(db.Boolean, nullable=False, index=True, default=1)

    def to_json(self):
        json_user = {
            #'url': url_for('api.get_user', id=self.id),
            'id'        : self.id,
            'keyname'   : self.keyname,
            'active'    : self.active,
        }
        return json_user

    def __repr__(self):
        return '<UserModel %r>' % (self.id)
