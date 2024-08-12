#!/usr/bin/python3
"Implementations for all default RESTful API methods for States"
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def retrieve_all_states():
    "fetch all state objects"
    all_states = storage.all(State).values()
    return jsonify([s.to_dict() for s in all_states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def fetch_state(state_id):
    "fetch a state obj"
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    return jsonify(st.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """Delete a State object"""
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    storage.delete(st)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_new_state():
    """add new state"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    request_data = request.get_json()
    state_instance = State(**request_data)
    state_instance.save()
    return jsonify(state_instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object"""
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    d = request.get_json()
    for k, value in d.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(st, k, value)
    st.save()
    return jsonify(st.to_dict()), 200
