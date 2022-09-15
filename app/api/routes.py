from flask import Blueprint, request, jsonify
from models import db, Users, UserLocation, SavedOneLocation, SavedTwoLocation, SavedThreeLocation, user_schema, users_schema, location_schema
from helpers import user_token_required
import os
import requests


api = Blueprint('api', __name__, url_prefix='/api')

baseMapQuestURL = 'http://www.mapquestapi.com/geocoding/v1/address?'
mapQuestKey = os.environ.get('FLASK_MAP_KEY')
baseWeatherGov = 'https://api.weather.gov/points'
baseWeatherGovForecast = 'https://api.weather.gov/gridpoints/'

def get_grid_points(city, state):
    map_quest = requests.get(f'{baseMapQuestURL}location={city},{state}&key={mapQuestKey}')
    lat_long = map_quest.json()
    grid_points_request = requests.get(f'{baseWeatherGov}/{lat_long["results"][0]["locations"][0]["latLng"]["lat"]},{lat_long["results"][0]["locations"][0]["latLng"]["lng"]}')
    grid_points_json = grid_points_request.json()
    grid_points = {
                    "city": city,
                    "state": state,
                    "gridId": grid_points_json['properties']['gridId'],
                    "gridX": grid_points_json['properties']['gridX'],
                    "gridY": grid_points_json['properties']['gridY']  
                }
    
    
    return grid_points

# GET

@api.route('/', methods=['GET'])
def greeting():
    forecast_request = requests.get(f'{baseWeatherGovForecast}SEW/131,84/forecast')
    forecast_json = forecast_request.json()
  
    forecast = forecast_json['properties']['periods'][0]
    
    return forecast
    
    

@api.route('/user', methods=['GET'])
@user_token_required
def get_user(current_user_token):
    user = Users.query.filter_by(id=current_user_token.id).first()
    response = user_schema.dump(user)
    return jsonify(response)

@api.route('/user/forecast/<id>', methods=['GET'])
@user_token_required
def user_forecast(current_user_token, id):

    user_location = UserLocation.query.filter_by(user_id = id).first()
    forecast_request = requests.get(f'{baseWeatherGovForecast}{user_location.grid_id}/{user_location.grid_x},{user_location.grid_y}/forecast')
    forecast_json = forecast_request.json()
  
    forecast = forecast_json['properties']['periods'][0]
    
    return forecast



@api.route('saved/forecast/<num>/<id>', methods=['GET'])
def saved_forecast(num, id):
    saved = ''
    
    if num == '1':
        saved = SavedOneLocation.query.filter_by(user_id = id).first()
    elif num == '2':
        saved = SavedTwoLocation.query.filter_by(user_id = id).first()
    elif num == '3':
        saved = SavedThreeLocation.query.filter_by(user_id = id).first()
        
    forecast_request = requests.get(f'{baseWeatherGovForecast}{saved.grid_id}/{saved.grid_x},{saved.grid_y}/forecast')
    forecast_json = forecast_request.json()

    forecast = forecast_json['properties']['periods'][0]
    
    return forecast
    
@api.route('/saved/<num>/<id>', methods=['GET'])
def saved_info(num, id):
    saved = ''
    
    if num == '1':
        saved = SavedOneLocation.query.filter_by(user_id = id).first()
    elif num == '2':
        saved = SavedTwoLocation.query.filter_by(user_id = id).first()
    elif num == '3':
        saved = SavedThreeLocation.query.filter_by(user_id = id).first()
    
    response = location_schema.dump(saved)
    return jsonify(response)

@api.route('/profile/<id>', methods=['GET'])
@user_token_required
def get_profile(current_user_token, id):
    profile = UserLocation.query.filter_by(user_id = id).first()

    response = location_schema.dump(profile)
    
    return jsonify(response)

# POST
@api.route('/userlocal', methods=['POST'])
def create_user():
    id = request.json['id']
    city = request.json['city']
    state = request.json['state']

    grid_points = get_grid_points(city, state)

    location = UserLocation(id, city, state, grid_points["gridId"], grid_points['gridX'], grid_points["gridY"])
    db.session.add(location)
    
    user = Users(id, location.user_location_id)
  
    db.session.add(user)
    db.session.commit()
    
    response = user_schema.dump(user)
    return jsonify(response)

@api.route('/saved/<num>/<id>', methods=['POST'])
def create_saved(num, id):
    city = request.json['city']
    state = request.json['state']
    
    grid_points = get_grid_points(city, state)
    
    location = ''
    
    if num == '1':
        location = SavedOneLocation(id, city, state, grid_points["gridId"], grid_points['gridX'], grid_points["gridY"])
    elif num == '2':
        location = SavedTwoLocation(id, city, state, grid_points["gridId"], grid_points['gridX'], grid_points["gridY"])
    elif num == '3':
        location = SavedThreeLocation(id, city, state, grid_points["gridId"], grid_points['gridX'], grid_points["gridY"])
        
    db.session.add(location)
    db.session.commit()
    
    response = location_schema.dump(location)
    return jsonify(response)

# PUT
@api.route('/profile/<id>', methods=['PUT'])
@user_token_required
def update_user_location(current_user_token, id):
    profile = UserLocation.query.filter_by(user_id = id).first()
    city = request.json['city']
    state = request.json['state']
    
    grid_points = get_grid_points(city, state)
    
    profile.city = city
    profile.state = state
    profile.grid_id = grid_points['gridId']
    profile.grid_x = grid_points['gridX']
    profile.grid_y = grid_points['gridY']
    
    db.session.commit()
    
    response = location_schema.dump(profile)
    return jsonify(response)

@api.route('/saved/<num>/<id>', methods=['PUT'])
def update_saved_location( num, id):
    city = request.json['city']
    state = request.json['state']
    location = ''
    
    if num == '1':
        location = SavedOneLocation.query.filter_by(user_id = id).first()
    elif num == '2':
        location = SavedTwoLocation.query.filter_by(user_id = id).first()
    elif num == '3':
        location = SavedThreeLocation.query.filter_by(user_id = id).first()
    
    grid_points = get_grid_points(city, state)
        
    location.city = city
    location.state = state
    location.grid_id = grid_points['gridId']
    location.grid_x = grid_points['gridX']
    location.grid_y = grid_points['gridY']
    
    db.session.commit()
    
    response = location_schema.dump(location)

    return jsonify(response)
    