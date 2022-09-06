from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from uuid import uuid4
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

class Users(db.Model):
    id = db.Column(db.String, primary_key=True)
    location = db.Column(db.String, nullable=True, default="")
    saved_1 = db.Column(db.String, nullable=True, default="")
    saved_2 = db.Column(db.String, nullable=True, default="")
    saved_3 = db.Column(db.String, nullable=True, default="")
    
    def __init__(self, id, location, saved_1='', saved_2='', saved_3=''):
        self.id = id
        self.location = location
        self.saved_1 = saved_1
        self.saved_2 = saved_2
        self.saved_3 = saved_3
        
    def __repr__(self):
        return f"User {self.id} has been added to the database"
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'location', 'saved_1', 'saved_2', 'saved_3']
        
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)
    