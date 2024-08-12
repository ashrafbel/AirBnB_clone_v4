#!/usr/bin/python3
"""Handles RESTful API actions for Place objects"""
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage
from models.city import City
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    "Get all Place objects for a specific City"
    Ct = storage.get(City, city_id)
    if not Ct:
        abort(404)
    P = [place.to_dict() for place in Ct.places]
    return jsonify(P)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieve a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """Delete a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def new_place(city_id):
    """Create a Place"""
    Ct = storage.get(City, city_id)
    if not Ct:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    info = request.get_json()
    if 'user_id' not in info:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, info['user_id'])
    if not user:
        abort(404)
    if 'name' not in info:
        return jsonify({"error": "Missing name"}), 400
    info['city_id'] = city_id
    new_place_created = Place(**info)
    new_place_created.save()
    return jsonify(new_place_created.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Update a Place object"""
    P = storage.get(Place, place_id)
    if not P:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    info = request.get_json()
    for key, val in info.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(P, key, val)
    P.save()
    return jsonify(P.to_dict()), 200
