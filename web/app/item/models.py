from flask import url_for
from datetime import datetime
from .. import db


class ItemModel(db.Model):
    __tablename__ = 'item'
    id         = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    keyname    = db.Column(db.String(63), nullable=False, index=True, unique=True, default='')
    mod_create = db.Column(db.DateTime, default=datetime.utcnow)

    def to_json(self):
        json_item = {
            #'url': url_for('api.get_item', id=self.id),
            'id'        : self.id,
            'keyname'   : self.keyname,
            'mod_create': self.mod_create,
        }
        return json_item

    def __repr__(self):
        return '<Item %r>' % (self.id)
