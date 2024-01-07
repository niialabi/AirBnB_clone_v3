#!/usr/bin/python3
""" flask API """

from flask import Flask
from api.v1.views import app_views

app = Flask(__name__)

app.register_blueprint(app_views, url_prefix='/app')

@app.route("/", strict_slashes=False)
def hello():
    """ displays Hello HBNB! """
    return "Hello HBNB!"


@app.teardown_appcontext

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
