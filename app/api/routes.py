from flask import Blueprint, request, jsonify
from models import db, Users, user_schema, users_schema
from helpers import user_token_required


api = Blueprint('api', __name__, url_prefix='/api')

# GET
@api.route('/', methods=['GET'])
def all_users():
    users = Users.query.all()
    response = users_schema.dump(users)
    return jsonify(response)

@api.route('/user', methods=['GET'])
@user_token_required
def get_user(current_user_token):
    user = Users.query.filter_by(id=current_user_token.id).first()
    response = user_schema.dump(user)
    return jsonify(response)

# POST
@api.route('/user', methods=['POST'])
def create_user():
    id = request.json['id']
    location = request.json['location']
    saved_1 = request.json['saved_1']
    saved_2 = request.json['saved_2']
    saved_3 = request.json['saved_3']
    
    user = Users(id, location, saved_1, saved_2, saved_3)
    
    db.session.add(user)
    db.session.commit()
    
    response = user_schema.dump(user)
    return jsonify(response)