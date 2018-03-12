from flask import url_for
from datetime import datetime
from .. import db


class ItemModel(db.Model):
    __tablename__ = 'item'
    id         = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    keyname    = db.Column(db.String(63), nullable=False, index=True, unique=True, default='')
    active     = db.Column(db.Boolean, nullable=False, index=True, default=1)
    item_title = db.Column(db.String(255))
    item_text  = db.Column(db.Text)
    mod_create = db.Column(db.DateTime, default=datetime.utcnow)
    mod_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

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
        }
        return json_item

    def __repr__(self):
        return '<ItemModel: id="%r", keyname="%r">' % (self.id, self.keyname)

    def __str__(self):
        return 'Item: "%r"' % (self.keyname)
