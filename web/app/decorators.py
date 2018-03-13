import logging
from functools import wraps

from flask import request, session
from . import db

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


# create session values for list select options
# from ..decorators import get_list_opts
# @get_list_opts(ItemModel,'item_list_opts')
def get_list_opts( model, session_key='list_opts' ):
    def _decorator(f):
        @wraps(f)
        def _decorated(*args, **kwargs):

            # set default values
            if not session_key in session:
                logging.debug('create session[%s]' % (session_key))
                session[session_key] = { \
                    'itemcnt' : 0, \
                    'status'  : 'all', \
                    'sort'    : 'id', \
                    'order'   : 'asc', \
                    'offset'  : 0, \
                    'limit'   : 0, \
                    }

            # get updates
            S = session[session_key]
            status = request.values.get('status', S['status'])
            sort   = request.values.get('sort',   S['sort'])
            order  = request.values.get('order',  S['order'])
            offset = int(request.values.get('offset',  S['offset']))
            limit  = int(request.values.get('limit', S['limit']))

            S['itemcnt'] = db.session.query(model).count()
            if status in ['all','active','inactive']:
                S['status'] = status
            if len(sort) > 0 and sort != S['sort']:
                S['sort']  = sort
                S['order'] = 'asc'
            elif order in ['asc','desc']:
                S['order'] = order

            if limit > 0 and limit != S['limit']:
                S['limit'] = limit
            if offset > 0 and offset != S['offset']:
                S['offset'] = offset

            # set result
            session[session_key] = S

            return f(*args, **kwargs)
        return _decorated
    return _decorator
