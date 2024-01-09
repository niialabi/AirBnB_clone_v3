#!/usr/bin/python3
""" reviews api """
from flask import abort, make_response, request
from models.review import Review
from models import storage
from models.user import User
from api.v1.views import app_views
from models.place import Place

import json


@app_views.route("/places/<id_place>/reviews", methods=["GET"])
def get_reviews(id_place):
    """ retrieves all reviews """
    place = storage.get(Place, id_place)
    reviewsList = []
    if not place:
        abort(404)
    for review in place.reviews:
        reviewsList.append(review.to_dict())
    out = reviewsList
    output = make_response(json.dumps(out), 200)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/reviews/<id>", methods=["GET"])
def get_review(id):
    """ retrieves rev with<id> """
    review = storage.get(Review, id)
    if not review:
        abort(404)
    response_data = review.to_dict()
    output = make_response(json.dumps(response_data), 200)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/reviews/<id>", methods=["DELETE"])
def delete_review(id):
    """ deletes review <id> """
    review = storage.get(Review, id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    out = {}
    output = make_response(json.dumps(out), 200)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/places/<id_place>/reviews", methods=["POST"])
def create_review(id_place):
    """ inserts reviews<id> """
    missiing_id = "Missing user_id"
    missing_text = "Missing text"
    place = storage.get(Place, id_place)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if "user_id" not in data:
        abort(400, description=missiing_id)
    if not storage.get(User, data.get("user_id")):
        abort(404)
    if "text" not in data:
        abort(400, description=missing_text)
    input_insert_obj = Review(**data)
    input_insert_obj.place_id = id_place
    input_insert_obj.save()
    out = input_insert_obj.to_dict()
    output = make_response(json.dumps(out), 201)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/reviews/<id>", methods=["PUT"])
def put_review(id):
    """ update reviews<id> """
    not_json = "Not a JSON"
    review = storage.get(Review, id)
    ignoreKeys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description=not_json)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignoreKeys:
            setattr(review, key, value)
    storage.save()
    out = review.to_dict()
    output = make_response(json.dumps(out), 200)
    output.headers["Content-Type"] = "application/json"
    return output
