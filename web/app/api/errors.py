from flask import jsonify, request

def unauthorized(message):
    response = jsonify({ \
        'code': 401, 'name': 'Unauthorized', 'message': message, 'url': request.url \
        #, 'request': dir(request) \
        })
    response.status_code = 401
    return response

def forbidden(message):
    response = jsonify({ \
        'code': 403, 'name': 'Forbidden', 'message': message, 'url': request.url \
        #, 'request': dir(request) \
        })
    response.status_code = 403
    return response

