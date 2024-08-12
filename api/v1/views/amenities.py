#!/usr/bin/python3
"""Amenities module for route web"""
from flask import jsonify, request, abort
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def retrieve_all_amenities():
    """Fetch the complete list of all Amenity objects"""
    a = [am.to_dict() for am in storage.all(Amenity).values()]
    return jsonify(a)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def fetch_amenity(amenity_id):
    """Fetch a single Amenity object"""
    a = storage.get(Amenity, amenity_id)
    if not a:
        abort(404)
    return jsonify(a.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """remove an Amenity object"""
    a = storage.get(Amenity, amenity_id)
    if not a:
        abort(404)
    storage.delete(a)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Create a new Amenity"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    amenity_info = request.get_json()
    namenity = Amenity(**amenity_info)
    namenity.save()
    return jsonify(namenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Update an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    amenity_info = request.get_json()
    for k, value in amenity_info.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
