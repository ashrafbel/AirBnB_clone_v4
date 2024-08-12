#!/usr/bin/python3
"""Review module for handling RESTful API actions"""
from flask import jsonify, request, abort
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def retrieve_all__reviews(place_id):
    "fetch all state objects"
    p = storage.get(Place, place_id)
    if not p:
        abort(404)
    rs = [review.to_dict() for review in p.reviews]
    return jsonify(rs)


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def fetch_review(review_id):
    """fetch Review object"""
    r = storage.get(Review, review_id)
    if not r:
        abort(404)
    return jsonify(r.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """remove a Review object"""
    r = storage.get(Review, review_id)
    if not r:
        abort(404)
    storage.delete(r)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_nwe_review(place_id):
    """Create new a Review"""
    p = storage.get(Place, place_id)
    if not p:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    info = request.get_json()
    if 'user_id' not in info:
        return jsonify({"error": "Missing user_id"}), 400
    user = storage.get(User, info['user_id'])
    if not user:
        abort(404)
    if 'text' not in info:
        return jsonify({"error": "Missing text"}), 400
    info['place_id'] = place_id
    new_review = Review(**info)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Update a Review object"""
    rw = storage.get(Review, review_id)
    if not rw:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    info = request.get_json()
    for k, v in info.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(rw, k, v)
    rw.save()
    return jsonify(rw.to_dict()), 200
