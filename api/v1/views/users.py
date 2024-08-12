#!/usr/bin/python3
"Module for handling RESTful API actions related to User objects"
from flask import jsonify, request, abort
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def retrieve_all_users():
    "Retrieve all User objects"
    us = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(us)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def retrieve_user(user_id):
    """Retrieve a User object"""
    u = storage.get(User, user_id)
    if not u:
        abort(404)
    return jsonify(u.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Delete a User object"""
    u = storage.get(User, user_id)
    if not u:
        abort(404)
    storage.delete(u)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create new User"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in request.json:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in request.json:
        return jsonify({"error": "Missing password"}), 400
    user_info = request.get_json()
    create_new_user = User(**user_info)
    create_new_user.save()
    return jsonify(create_new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """Update a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    user_info = request.get_json()
    for key, val in user_info.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_dict()), 200
