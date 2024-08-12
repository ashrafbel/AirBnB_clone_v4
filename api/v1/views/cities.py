#!/usr/bin/python3
"Cities module for route web"
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def retrieve_all_cities(state_id):
    "Get all City objects for a specific State"
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    city_objects = [city.to_dict() for city in st.cities]
    return jsonify(city_objects)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def fetch_city(city_id):
    """fetch a City object"""
    ct = storage.get(City, city_id)
    if not ct:
        abort(404)
    return jsonify(ct.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """remove a City object"""
    ct = storage.get(City, city_id)
    if not ct:
        abort(404)
    storage.delete(ct)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    "add new city"
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    city_info = request.get_json()
    city_info['state_id'] = state_id
    add_new_city = City(**city_info)
    add_new_city.save()
    return jsonify(add_new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Update a City object"""
    ct = storage.get(City, city_id)
    if not ct:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    city_info = request.get_json()
    for key, val in city_info.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(ct, key, val)
    ct.save()
    return jsonify(ct.to_dict()), 200
