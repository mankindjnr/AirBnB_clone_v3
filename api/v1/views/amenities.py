#!/usr/bin/python3

"""
a state blueprint
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models import State
from models import City
from models import Amenity


@app_views.route('/amenities/', methods=["GET"], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def amenities(amenity_id=None):
    """retrieving a list of all amenity objects"""

    if amenity_id is None:
        the_amenities = storage.all("Amenity")
        amenities = [value.to_dict() for key, value in the_amenities.items()]
        return jsonify(amenities)

    amenities = storage.get("Amenity", amenity_id)
    if amenities is None:
        abort(404)

    return jsonify(amenities.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """deleting an amenity based on its id"""

    amenities = storage.get("Amenity", amenity_id)
    if amenities is None:
        abort(404)

    amenities.delete()
    return jsonify({})


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """create a new amenity"""

    the_content = request.get_json()
    if the_content is None:
        return (jsonify({"error": "Not a JSON"}), 400)
    name = the_content.get("name")
    if name is None:
        return (jsonify({"error": "Missing name"}), 400)

    a_new_amenity = Amenity()
    a_new_amenity.name = name
    a_new_amenity.save()
    return (jsonify(a_new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """updating an amenity"""

    the_content = request.get_json()
    if the_content is None:
        return (jsonify({"error": "Not a JSON"}), 400)

    an_amenity = storage.get("Amenity", amenity_id)
    if an_amenity is None:
        abort(404)

    not_allowed = ["id", "created_at", "updated_at"]
    for key, value in the_content.items():
        if key not in not_allowed:
            setattr(an_amenity, key, value)

    an_amenity.save()
    return jsonify(an_amenity.to_dict())
