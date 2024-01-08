#!/usr/bin/python3
""" states api """
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, make_response, request
import json


@app_views.route('/states', methods=['GET'])
def get_states():
    """ Retrieves the list of all State objects """
    all_states = storage.all(State).values()
    list_of_states = []
    for state in all_states:
        list_of_states.append(state.to_dict())
    output = make_response(json.dumps(list_of_states), 200)
    output.headers["Content-type"] = "application/json"
    return output


@app_views.route('/states/<id>', methods=['GET'])
def get_states_id(id):
    """ Retrieves a specific State object by ID. """
    state_id = storage.get(State, id)
    if not state_id:
        abort(404)
    state_dict = state_id.to_dict()
    output = make_response(json.dumps(state_dict), 200)
    output.headers["Content-type"] = "application/json"
    return output


@app_views.route("/states/<id>", methods=["DELETE"])
def delete_state(id):
    """ deletes state <id> """
    state_to_del = storage.get(State, id)
    if not state_to_del:
        abort(404)
    storage.delete(state_to_del)
    storage.save()
    out = {}
    output = make_response(json.dumps(out), 200)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/states", methods=["POST"])
def create_state():
    """ Inserts state if valid json with has correct key """
    not_json = "Not a JSON"
    not_name = "Missing name"
    if not request.get_json():
        abort(400, description=not_json)
    if "name" not in request.get_json():
        abort(400, description=not_name)
    u_input = request.get_json()
    input_insert_obj = State(**u_input)
    input_insert_obj.save()
    out = input_insert_obj.to_dict()
    output = make_response(json.dumps(out), 201)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/states/<id>", methods=["PUT"])
def put_state(id):
    """update a state by id"""
    not_json = "Not a JSON"
    state = storage.get(State, id)
    key_exeption = ["id", "created_at", "updated_at"]
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description=not_json)
    u_input = request.get_json()
    for key, value in u_input.items():
        if key not in key_exeption:
            setattr(state, key, value)
    storage.save()
    out = state.to_dict()
    output = make_response(json.dumps(out), 200)
    output.headers["Content-Type"] = "application/json"
    return output
