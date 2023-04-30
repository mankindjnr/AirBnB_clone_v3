#!/usr/bin/python3
"""
importing a blueprint of the from the flask doc
"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """
    return the state
    """
    return (jsonify({"status": "OK"}))


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    returns the states
    """
    return jsonify({"amenities": storage.obj_count("Amenity"),
                    "cities": storage.obj_count("City"),
                    "places": storage.obj_count("Place"),
                    "reviews": storage.obj_count("Review"),
                    "states": storage.obj_count("State"),
                    "users": storage.obj_count("User")
    })
