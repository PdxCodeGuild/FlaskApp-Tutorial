from flask import url_for
from datetime import datetime
from .. import db
from ..user.models import UserModel


def get_owner_id_choices():
    result = []
    rows = UserModel.query.order_by(getattr( UserModel, 'keyname' ).asc())
    for row in rows:
        result.append((row.id, "%s (%s)" % (row.keyname,row.user_email)))
    return result


class ItemModel(db.Model):
    __tablename__ = 'item'
    id         = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    active     = db.Column(db.Boolean, nullable=False, index=True, default=1)
    keyname    = db.Column(db.String(63), nullable=False, index=True, unique=True, default='')
    item_title = db.Column(db.String(255))
    item_text  = db.Column(db.Text)
    mod_create = db.Column(db.DateTime, default=datetime.utcnow)
    mod_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # 'back_populates' requires reciprocal relationship in UserModel ; 'backref' creates both sides
    # @see http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html
    owner_id   = db.Column(db.Integer, db.ForeignKey('user.id'))
    #owner      = db.relationship('UserModel', back_populates='items')
    owner      = db.relationship('UserModel', backref='items')

    def to_json(self):
        json_item = {
            #'url': url_for('api.get_item', id=self.id),
            'id'        : self.id,
            'keyname'   : self.keyname,
            'active'    : self.active,
            'item_title': self.item_title,
            'item_text' : self.item_text,
            'mod_create': self.mod_create,
            'mod_update': self.mod_update,
            #'owner_url': url_for('api.get_user', id=self.owner_id),
            'owner_id'  : self.owner_id,
        }
        return json_item

    def __repr__(self):
        return '<ItemModel: id="%r", keyname="%r">' % (self.id, self.keyname)

    def __str__(self):
        return 'Item: "%r"' % (self.keyname)
