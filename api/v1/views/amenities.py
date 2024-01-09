#!/usr/bin/python3
""" Amenity API views """
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """ Retrieves the list of all Amenity objects """
    amenities = storage.all(Amenity).values()
    return jsonify([amenity.to_dict() for amenity in amenities])


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """ Retrieves a specific Amenity object by ID """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """ Deletes a specific Amenity object by ID """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """ Creates a new Amenity object """
    not_json = "Not a JSON"
    missing_name = "Missing name"
    if not request.get_json():
        abort(400, description=not_json)
    data = request.get_json()
    if "name" not in data:
        abort(400, description=missing_name)
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates a specific Amenity object by ID """
    not_json = "Not a JSON"
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description=not_json)
    data = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200

