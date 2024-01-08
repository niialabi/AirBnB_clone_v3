#!/usr/bin/python3
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
<<<<<<< HEAD
from api.v1.views.cities import *
from api.v1.views.users import *
=======
from api.v1.views.amenities import *
>>>>>>> 8c99ddef2b18c0cd0f923a3882448559fab5ba47
