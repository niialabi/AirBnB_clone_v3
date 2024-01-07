#!/usr/bin/python3
from flask import Blueprint, render_template

app_views = Blueprint('app_views', __name__)

@app_views.route('/home')
def home():
    return render_template('home.html')
