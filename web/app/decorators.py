import logging
from functools import wraps

from flask import request, session
from flask_login import current_user
from . import config_default as CONFIG
from . import db, login_manager


# @my_decorator('myvalue')
def my_decorator(key='some value'):
    def _decorator(f):
        @wraps(f)
        def _decorated(*args, **kwargs):
            logging.debug('my_decorator( %s )' % (key))
            return f(*args, **kwargs)
        return _decorated
        #return wraps(f)(_decorated)
    return _decorator


# check current user_role >= requested role
# if not logged in return unauthorized() ; if not allowed: return needs_refresh()
def role_required( role=CONFIG.USER_ROLE_VIEW ):
    def _decorator(f):
        @wraps(f)
        def _decorated(*args, **kwargs):
            if not current_user.is_active:
                logging.info('role_required( %s ) - unauthorized' % (role))
                return login_manager.unauthorized()
            if current_user.user_role < role:
                logging.info('role_required( %s < %s ) - needs_refresh' % (current_user.user_role,role))
                return login_manager.needs_refresh()
            logging.debug('role_required( %s >= %s )' % (CONFIG.USER_ROLE[current_user.user_role],CONFIG.USER_ROLE[role]))
            return f(*args, **kwargs)
        return _decorated
    return _decorator


# create session values for list select options
# from ..decorators import get_list_opts
# @get_list_opts(ItemModel,'item_list_opts')
def get_list_opts( session_key='list_opts' ):
    def _decorator(f):
        @wraps(f)
        def _decorated(*args, **kwargs):

            # set default values
            if not session_key in session:
                logging.debug('create session[%s]' % (session_key))
                session[session_key] = { \
                    'itemcnt'     : 0, \
                    'pagecnt'     : 0, \
                    'user_role'   : -1, \
                    'item_status' : -1, \
                    'sort'        : 'id', \
                    'order'       : 'asc', \
                    'offset'      : 0, \
                    'limit'       : 10, \
                    'page'        : 1, \
                    }

            # get updates
            S = session[session_key]
            user_role   = request.values.get('user_role',   S['user_role'])
            item_status = request.values.get('item_status', S['item_status'])
            sort        = request.values.get('sort',        S['sort'])
            order       = request.values.get('order',       S['order'])
            limit       = int(request.values.get('limit',   S['limit']))
            page        = int(request.values.get('page',    S['page']))

            if user_role in [-1,0,1,2,3]:
                S['user_role'] = int(user_role)
            if item_status in [-1,0,1,2,3]:
                S['item_status'] = item_status
            if len(sort) > 0 and sort != S['sort']:
                S['sort']  = sort
                S['order'] = 'asc'
            elif order in ['asc','desc']:
                S['order'] = order

            if limit > 0 and limit != S['limit']:
                S['limit'] = limit
            if page > 0 and page != S['page']:
                S['page'] = page

            # set result
            session[session_key] = S

            return f(*args, **kwargs)
        return _decorated
    return _decorator
