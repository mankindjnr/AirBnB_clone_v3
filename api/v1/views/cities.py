#!/usr/bin/python3

"""
handles apiu action for sta
"""

from api.v1.views import app_views
from flask import request, jsonify, abort
from models.state import State
from models import storage
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET', 'POST'], strict_slashes=False)
def retrieve_cities(state_id):
    """retrieve cities by their id """
    state_objects = storage.all(State)
    states = [obj for obj in state_objects.values()]

    if request.method == 'GET':
        for state in states:
            if state.id == state_id:
                cities_objs = storage.all(City)
                cities = [obj.to_dict() for obj in
                          cities_objs.values() if obj.state_id == state_id]
                return jsonify(cities)
        abort(404)
    elif request.method == 'POST':
        for state in states:
            if state.id == state_id:
                dictionary = request.get_json()
                if dictionary is None:
                    abort(400, 'Not a JSON')
                if dictionary.get("name") is None:
                    abort(400, 'Missing name')
                dictionary["state_id"] = state_id
                city = City(**dictionary)
                city.save()
                return jsonify(city.to_dict()), 201
        abort(404)


@app_views.route('/cities/<string:city_id>',
                 methods=['GET', 'PUT', 'DELETE'], strict_slashes=False)
def city_city_id(city_id):
    """retrieve by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        dictionary = request.get_json()
        if dictionary is None:
            abort(400, 'Not a JSON')
        city.name = dictionary.get("name")
        city.save()
        return jsonify(city.to_dict()), 200
