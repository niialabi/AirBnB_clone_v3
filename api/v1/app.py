#!/usr/bin/python3
""" flask API """

from flask import Flask
from models import storage
from api.v1.views import app_views
from flask import Blueprint
from flask_cors import CORS
import os

app = Flask(__name__)

app.register_blueprint(app_views)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})

@app.teardown_appcontext
def close_storage(exception):
    """ closes storage """
    from models import storage

    storage.close()


@app.errorhandler(404)
def not_found(error):
    """ Returns JSON response with 404 status """
    from flask import make_response, jsonify

    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = os.environ.get('HBNB_API_PORT', '5000')

    app.run(host=host, port=port, threaded=True)
