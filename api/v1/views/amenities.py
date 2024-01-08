#!/usr/bin/python3
""" View for Amenity objects that handles default API actions """
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'])
def amenities():
    """ Retrieves the list of all Amenity objects """
    list_amenities = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in list_amenities.values()])


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def r_amenity_id(amenity_id):
    """ Retrieves Amenity object """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def del_amenity(amenity_id):
    """ Deletes a Amenity object """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        return error_response(404, 'Amenity not found')
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def post_amenity():
    """ Creates a Amenity object """
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if "name" not in new_amenity:
        abort(400, "Missing name")
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """ Updates an Amenity object """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        return error_response(404, 'Amenity not found')

    body_request = request.get_json()
    if not body_request:
        return error_response(400, 'Not a JSON')

    for key, value in body_request.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
