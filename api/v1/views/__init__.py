#!/usr/bin/python3
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
<<<<<<< HEAD
from api.v1.views.amenities import *
=======
from api.v1.views.cities import *
>>>>>>> a87ed3557a0465c28a9f8c4a455c9d824da702c9
