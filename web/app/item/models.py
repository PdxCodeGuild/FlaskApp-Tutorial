import logging
from flask import url_for
from datetime import datetime
from sqlalchemy.ext.associationproxy import association_proxy
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
    id          = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    item_status = db.Column(db.SmallInteger, nullable=False, index=True, default=1)
    keyname     = db.Column(db.String(63), nullable=False, index=True, unique=True, default='')
    item_title  = db.Column(db.String(255))
    item_text   = db.Column(db.Text)
    mod_create  = db.Column(db.DateTime, default=datetime.utcnow)
    mod_update  = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)

    # @see http://docs.sqlalchemy.org/en/latest/orm/relationship_api.html
    owner_id   = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner      = db.relationship('UserModel', backref='items')

    # association proxy of "item_users" collection to "users_id" attribute for EditItemForm
    # @see http://docs.sqlalchemy.org/en/rel_0_9/orm/extensions/associationproxy.html
    users_id = association_proxy('item_users', 'user.id')

    def to_json(self):
        json_item = {
            'url': url_for('api.get_item', id=self.id, _external=True),
            'id'         : self.id,
            'keyname'    : self.keyname,
            'item_status': self.item_status,
            'item_title' : self.item_title,
            'item_text'  : self.item_text,
            'mod_create' : self.mod_create,
            'mod_update' : self.mod_update,
            'url_owner'  : url_for('api.get_item_owner', id=self.id, _external=True),
            'owner_id'   : self.owner_id,
            'url_editor' : url_for('api.get_item_editor', id=self.id, _external=True),
            'editor_id'  : [iu.user_id for iu in self.item_users]
        }
        return json_item

    def __init__(self, **kwargs):
        super(ItemModel, self).__init__(**kwargs)
        self.id          = kwargs.get('id',          None)
        self.keyname     = kwargs.get('keyname',     None)
        self.item_status = kwargs.get('item_status', 1)
        self.item_title  = kwargs.get('item_title',  None)
        self.item_text   = kwargs.get('item_text',   0)
        self.mod_create  = kwargs.get('mod_create',  None)
        self.mod_update  = kwargs.get('mod_update',  None)
        logging.debug( "ItemModel.__init__: %r" %  (self))
        logging.debug( "ItemModel.__init__: owner=%r" %  (self.owner))
        logging.debug( "ItemModel.__init__: item_users=%r" %  (self.item_users))

    def __repr__(self):
        return '<ItemModel(id=%r,keyname=%r,item_status=%r,item_title=%r,item_text=%r,mod_create=%r,mod_update=%r)>' \
                % (self.id,self.keyname,self.item_status,self.item_title,self.item_text,self.mod_create,self.mod_update)

    def __str__(self):
        return 'ItemModel:%r,%r' % (self.id,self.keyname)


class ItemUserModel(db.Model):
    __tablename__ = 'item_user'
    item_id  = db.Column(db.BigInteger, db.ForeignKey('item.id'), primary_key=True)
    user_id  = db.Column(db.BigInteger, db.ForeignKey('user.id'), primary_key=True)
    relation = db.Column(db.String(31), nullable=False, default='editor')

    item = db.relationship("ItemModel", backref='item_users')
    user = db.relationship("UserModel", backref='user_items')

    def __init__(self, **kwargs):
        super(ItemUserModel, self).__init__(**kwargs)
        self.item_id = kwargs.get('item_id', None)
        self.user_id = kwargs.get('user_id', None)
        self.relation = kwargs.get('relation', 'editor')
        logging.debug( "ItemUserModel.__init__: %r" %  (self))
        logging.debug( "ItemUserModel.__init__: item=%r" %  (self.item))
        logging.debug( "ItemUserModel.__init__: user=%r" %  (self.user))

    def __repr__(self):
        return '<ItemUserModel(item_id=%r,user_id=%r,relation=%r)>' % (self.item_id,self.user_id,self.relation)

    def __str__(self):
        return 'ItemUserModel:%r,%r,%r' % (self.item_id,self.user_id,self.relation)

