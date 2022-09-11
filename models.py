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
    location_id = db.Column(db.String, nullable=True, default="")
    saved_1_id = db.Column(db.String, nullable=True, default="")
    saved_2_id = db.Column(db.String, nullable=True, default="")
    saved_3_id = db.Column(db.String, nullable=True, default="")
    
    def __init__(self, id, location_id, saved_1_id='', saved_2_id='', saved_3_id=''):
        self.id = id
        self.location_id = location_id
        self.saved_1_id = saved_1_id
        self.saved_2_id = saved_2_id
        self.saved_3_id = saved_3_id
        
    def __repr__(self):
        return f"User {self.id} has been added to the database"

class UserLocation(db.Model):
    user_location_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    grid_id = db.Column(db.String, nullable=False)
    grid_x = db.Column(db.Float, nullable=False)
    grid_y = db.Column(db.Float, nullable=False)
    
    def __init__(self, user_id, city, state, grid_id, grid_x, grid_y):
        self.user_location_id = self.set_id()
        self.user_id = user_id
        self.city = city
        self.state = state
        self.grid_id = grid_id
        self.grid_x = grid_x
        self.grid_y = grid_y
        
    def set_id(self):
        return str(uuid4())
    
    def __repr__(self):
        return f"User Location has been added to the database"

class SavedOneLocation(db.Model):
    saved_1_location_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    grid_id = db.Column(db.String, nullable=False)
    grid_x = db.Column(db.Float, nullable=False)
    grid_y = db.Column(db.Float, nullable=False)
    
    def __init__(self, user_id, city, state, grid_id, grid_x, grid_y):
        self.saved_1_location_id = self.set_id()
        self.user_id = user_id
        self.city = city
        self.state = state
        self.grid_id = grid_id
        self.grid_x = grid_x
        self.grid_y = grid_y
        
    def set_id(self):
        return str(uuid4())
    
    def __repr__(self):
        return f"Saved 1 Location has been added to the database"
    
class SavedTwoLocation(db.Model):
    saved_2_location_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    grid_id = db.Column(db.String, nullable=False)
    grid_x = db.Column(db.Float, nullable=False)
    grid_y = db.Column(db.Float, nullable=False)
    
    def __init__(self, user_id, city, state, grid_id, grid_x, grid_y):
        self.saved_2_location_id = self.set_id()
        self.user_id = user_id
        self.city = city
        self.state = state
        self.grid_id = grid_id
        self.grid_x = grid_x
        self.grid_y = grid_y
        
    def set_id(self):
        return str(uuid4())
    
    def __repr__(self):
        return f"Saved 2 Location has been added to the database"
        
class SavedThreeLocation(db.Model):
    saved_3_location_id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    state = db.Column(db.String, nullable=False)
    grid_id = db.Column(db.String, nullable=False)
    grid_x = db.Column(db.Float, nullable=False)
    grid_y = db.Column(db.Float, nullable=False)
    
    def __init__(self, user_id, city, state, grid_id, grid_x, grid_y):
        self.saved_3_location_id = self.set_id()
        self.user_id = user_id
        self.city = city
        self.state = state
        self.grid_id = grid_id
        self.grid_x = grid_x
        self.grid_y = grid_y
        
    def set_id(self):
        return str(uuid4())
    
    def __repr__(self):
        return f"Saved 3 Location has been added to the database"

class UserSchema(ma.Schema):
    class Meta:
        fields = ['id', 'location_id', 'saved_1_id', 'saved_2_id', 'saved_3_id']

class LocationSchema(ma.Schema):
    class Meta:
        fields = ['city', 'state', 'grid_id', 'grid_x', 'grid_y']  
        
              

user_schema = UserSchema()
users_schema = UserSchema(many=True)
location_schema = LocationSchema()
    