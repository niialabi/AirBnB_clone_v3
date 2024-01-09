#!/usr/bin/python3
"""api users"""
from flask import abort, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User
import json


@app_views.route("/users", methods=["GET"])
def get_users():
    """ retrieves all user obj """
    all_users = storage.all(User).values()
    user_list = []
    for user in all_users:
        user_list.append(user.to_dict())
    output = make_response(json.dumps(user_list), 200)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/users/<id>", methods=["GET"])
def get_user(id):
    """ retrieves users obj using id """
    user = storage.get(User, id)
    if not user:
        abort(404)
    output_data = user.to_dict()
    output = make_response(json.dumps(output_data), 200)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/users/<id>", methods=["DELETE"])
def delete_user(id):
    """ deletes user<id> """
    user = storage.get(User, id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    out = {}
    output = make_response(json.dumps(out), 200)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/users", methods=["POST"])
def create_user():
    """ inserts user's key """
    not_json = "Not a JSON"
    missing_email = "Missing email"
    misssiong_pswd = "Missing password"
    if not request.get_json():
        abort(400, description=not_json)
    if "email" not in request.get_json():
        abort(400, description=missing_email)
    if "password" not in request.get_json():
        abort(400, description=misssiong_pswd)
    data = request.get_json()
    input_insert_obj = User(**data)
    input_insert_obj.save()
    out = input_insert_obj.to_dict()
    output = make_response(json.dumps(out), 201)
    output.headers["Content-Type"] = "application/json"
    return output


@app_views.route("/users/<id>", methods=["PUT"])
def put_user(id):
    """ update user by id """
    not_json = "Not a JSON"
    user = storage.get(User, id)
    ignoreKeys = ["id", "email", "created_at", "updated_at"]
    if not user:
        abort(404)
    if not request.get_json():
        abort(400, description=not_json)
    data = request.get_json()
    for key, value in data.items():
        if key not in ignoreKeys:
            setattr(user, key, value)
    storage.save()
    out = user.to_dict()
    output = make_response(json.dumps(out), 200)
    output.headers["Content-Type"] = "application/json"
    return output