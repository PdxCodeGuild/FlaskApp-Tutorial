import logging
from flask import current_app, url_for
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db, login_manager
#from ..item.models import ItemModel

# @see https://flask-login.readthedocs.io/
#@login_manager.request_loader
#def load_user_from_request(request):

@login_manager.user_loader
def load_user(user_id):
    logging.info( "load_user(%s)" %  user_id)
    return UserModel.query.filter_by(id=user_id).first()


class UserModel(db.Model):
    __tablename__ = 'user'
    id         = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    user_role  = db.Column(db.SmallInteger, nullable=False, index=True, default=1)
    keyname    = db.Column(db.String(63), nullable=False, index=True, unique=True, default='')
    user_email = db.Column(db.String(255), nullable=False, unique=True, index=True)
    user_pass  = db.Column(db.String(128))
    cnt_login  = db.Column(db.Integer, default=0)
    mod_login  = db.Column(db.DateTime)
    mod_create = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    mod_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, password):
        logging.debug( "password.setter(%s)" %  self.user_email)
        self.user_pass = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_pass, password)

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return self.anonymous

    def is_active(self):
        return (self.user_role > current_app.config['USER_ROLE_NONE'])

    def get_id(self):
        return self.id

    def generate_auth_token(self, expires):
        s = Serializer(current_app.config['SECRET_KEY'],expires_in=expires)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return UserModel.query.get(data['id'])

    def update_mod_login(self):
        self.cnt_login = self.cnt_login + 1
        self.mod_login = datetime.utcnow()
        db.session.add(self)
        db.session.commit()
        logging.debug( "update_mod_login(%s)" %  self.user_email)

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'id'        : self.id,
            'user_role' : self.user_role,
            'keyname'   : self.keyname,
            'user_email': self.user_email,
            'cnt_login' : self.cnt_login,
            'mod_login' : self.mod_login,
            'mod_create': self.mod_create,
            'mod_update': self.mod_update,
            'url_item_owner'   : url_for('api.get_user_item_owner', id=self.id, _external=True),
            'count_item_owner' : len(self.items),
            'url_item_editor'  : url_for('api.get_user_item_editor', id=self.id, _external=True),
            'count_item_editor': len(self.user_items)
        }
        return json_user

    def __init__(self, **kwargs):
        super(UserModel, self).__init__(**kwargs)
        self.id         = kwargs.get('id',        None)
        self.user_role  = kwargs.get('user_role', current_app.config['USER_ROLE_VIEW'])
        self.keyname    = kwargs.get('keyname',   None)
        self.user_email = kwargs.get('user_email',None)
        self.cnt_login  = kwargs.get('cnt_login', 0)
        self.mod_login  = kwargs.get('mod_login', None)
        self.mod_create = kwargs.get('mod_create',None)
        self.mod_update = kwargs.get('mod_update',None)
        logging.debug( "UserModel.__init__: %r" %  (self))
        logging.debug( "ItemModel.__init__: items=%r" %  (self.items))
        logging.debug( "ItemModel.__init__: user_items=%r" %  (self.user_items))

    def __repr__(self):
        return '<UserModel(id=%r,user_role=%r,keyname=%r,user_email=%r,cnt_login=%r,mod_login=%r,mod_create=%r,mod_update=%r)>' \
                % (self.id,self.user_role,self.keyname,self.user_email,self.cnt_login,self.mod_login,self.mod_create,self.mod_update)

    def __str__(self):
        return 'UserModel:%r,%r' % (self.id,self.keyname)

