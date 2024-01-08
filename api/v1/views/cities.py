#!/usr/bin/python3
""" states api """
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import abort, make_response, request
import json


@app_views.route("/states/<id_state>/cities", methods=["GET"])
def get_cities(id_state):
    """ retrieves state id obj """
    state = storage.get(State, id_state)
    list_of_cities = []
    if not state:
        abort(404)
    for city in state.cities:
        list_of_cities.append(city.to_dict())
    res = list_of_cities
    output = make_response(json.dumps(res), 200)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/cities/<id>", methods=["GET"])
def get_city(id):
    """ retrieves city obj by id """
    city = storage.get(City, id)
    if not city:
        abort(404)
    output_data = city.to_dict()
    output = make_response(json.dumps(output_data), 200)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/cities/<id>", methods=["DELETE"])
def del_city(id):
    """delets city with id"""
    city = storage.get(City, id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    res = {}
    output = make_response(json.dumps(res), 200)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/states/<id_state>/cities", methods=["POST"])
def create_city(id_state):
    """ inserts key and state id """
    not_json = "Missing name"
    not_name = "Not a JSON"
    state = storage.get(State, id_state)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description=not_name)
    if "name" not in request.get_json():
        abort(400, description=not_json)
    data = request.get_json()
    input_insert_obj = City(**data)
    input_insert_obj.state_id = id_state
    input_insert_obj.save()
    out = input_insert_obj.to_dict()
    output = make_response(json.dumps(out), 201)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/cities/<id>", methods=["PUT"])
def put_city(id):
    """ update city record by id """
    not_name = "Not a JSON"
    city = storage.get(City, id)
    ignoreKeys = ["id", "state_id", "created_at", "updated_at"]
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description=not_name)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignoreKeys:
            setattr(city, key, value)
    storage.save()
    out = city.to_dict()
    output = make_response(json.dumps(out), 200)
    output.headers["Content-Type"] = "application/json"
    return output
