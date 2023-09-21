from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity

@app_views.route('/places/<place_id>/amenities', methods=['GET', 'POST'])
def place_amenities(place_id):
    """Handle GET and POST requests for Place-Amenity relationships."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)

    if request.method == 'POST':
        amenity_id = request.get_json().get('amenity_id')
        if amenity_id is None:
            abort(400, description='Missing amenity_id in request JSON')

        amenity = storage.get(Amenity, amenity_id)
        if amenity is None:
            abort(404)

        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200

        place.amenities.append(amenity)
        storage.save()
        return jsonify(amenity.to_dict()), 201

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """Handle DELETE requests to remove Amenity from Place."""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if amenity not in place.amenities:
        abort(404)

    place.amenities.remove(amenity)
    storage.save()
    return jsonify({}), 200