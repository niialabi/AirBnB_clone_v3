#!/usr/bin/python3
""" states api """
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort, make_response, request
import json


@app_views.route('/amenties', methods=['GET'])
def get_amenities():
    """ Retrieves the list of all amenities objects """
    all_amenities = storage.all(Amenity).values()
    list_of_amenities = []
    for Amenity in all_amenities:
        list_of_amenities.append(Amenity.to_dict())
    output = make_response(json.dumps(list_of_amenities), 200)
    output.headers["Content-type"] = "application/json"
    return output


@app_views.route('/amenities/<id>', methods=['GET'])
def get_amenity_id(id):
    """ Retrieves a specific amenities object by ID. """
    amenity_id = storage.get(Amenity, id)
    if not amenity_id:
        abort(404)
    amenity_dict = amenity_id.to_dict()
    output = make_response(json.dumps(amenity_dict), 200)
    output.headers["Content-type"] = "application/json"
    return output


@app_views.route("/amenities/<id>", methods=["DELETE"])
def delete_amenities(id):
    """ deletes amenities <id> """
    amenity_to_del = storage.get(Amenity, id)
    if not amenity_to_del:
        abort(404)
    storage.delete(amenity_to_del)
    storage.save()
    out = {}
    output = make_response(json.dumps(out), 200)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/amenities", methods=["POST"])
def create_amenities():
    """ Inserts amenities if valid json with has correct key """
    not_json = "Not a JSON"
    not_name = "Missing name"
    if not request.get_json():
        abort(400, description=not_json)
    if "name" not in request.get_json():
        abort(400, description=not_name)
    u_input = request.get_json()
    input_insert_obj = Amenity(**u_input)
    input_insert_obj.save()
    out = input_insert_obj.to_dict()
    output = make_response(json.dumps(out), 201)
    output.headers["Content-Type"] = "application/json"
    return output

@app_views.route("/amenities/<id>", methods=["PUT"])
def put_amenities(id):
    """update a amenity by id"""
    not_json = "Not a JSON"
    amenity = storage.get(Amenity, id)
    key_exeption = ["id", "created_at", "updated_at"]
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description=not_json)
    u_input = request.get_json()
    for key, value in u_input.items():
        if key not in key_exeption:
            setattr(state, key, value)
    storage.save()
    out = amenity.to_dict()
    output = make_response(json.dumps(out), 200)
    output.headers["Content-Type"] = "application/json"
    return output
