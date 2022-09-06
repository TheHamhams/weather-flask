from functools import wraps
import secrets
from flask import request, jsonify, json
import decimal
from models import Users
import os


def user_token_required(our_flask_function):
    @wraps(our_flask_function)
    def decorated(*args, **kwargs):
        id = None
        
        if 'x-access-token' in request.headers:
            id = request.headers['x-access-token'].split(' ')[1]
        if not id:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            current_user_token = Users.query.filter_by(id = id).first()
            
        except:
            owner = Users.query.filter_by(id = id).first()
            
            if id != owner.id and secrets.compare_digest(id, owner.id):
                return jsonify({'message': 'Token is invalid'})
        return our_flask_function(current_user_token, *args, **kwargs)
    return decorated


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return str(obj)
        else:
            return super(JSONEncoder, self).default(obj)