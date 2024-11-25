from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Place, EntertainmentType, PlaceCategory
from utils import log_user_activity

# Namespace
api = Namespace('places', description='Operations related to places')

# DTO Definitions
place_dto = api.model('Place', {
    'id': fields.Integer(description='Unique ID of the place'),
    'name': fields.String(required=True, description='Name of the place'),
    'description': fields.String(required=True, description='Description of the place'),
    'location': fields.String(required=True, description='Location of the place'),
    'city': fields.String(required=True, description='City of the place'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'rating': fields.Float(required=True, description='Rating of the place (1.0 to 5.0)'),
    'entertainment_type_id': fields.Integer(required=True, description='Entertainment type ID linked to the place'),
    'category_id': fields.Integer(description='Category ID linked to the place'),
    'default_price': fields.Float(description='Default price for the place'),
    'images': fields.List(fields.String, description='List of image URLs for the place')
})

create_place_dto = api.model('CreatePlace', {
    'name': fields.String(required=True, description='Name of the place'),
    'location': fields.String(required=True, description='Location of the place'),
    'rating': fields.Float(required=True, description='Rating of the place (1.0 to 5.0)'),
    'entertainment_type_id': fields.Integer(required=True, description='Entertainment type ID linked to the place')
})



class PlacesResource(Resource):
    @log_user_activity('view_places')
    @api.marshal_list_with(place_dto, envelope='data')
    def get(self):
        """Fetch all places"""
        try:
            places = Place.query.all()
            return places, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching places: %s', str(e))
            return {'message': 'Failed to fetch places. Please try again.'}, 500

    @log_user_activity('create_place')
    @jwt_required()
    @api.expect(create_place_dto, validate=True)
    def post(self):
        """Create a new place"""
        data = api.payload
        try:
            location_ = data['location'] if 'location' in data else None
            latitude_ = data['latitude'] if 'latitude' in data else None
            longitude_ = data['longitude'] if 'longitude' in data else None

            if not (1.0 <= data['rating'] <= 5.0):
                return {'message': 'Rating must be between 1.0 and 5.0'}, 400

            entertainment_type = EntertainmentType.query.get(data['entertainment_type_id'])
            if not entertainment_type:
                return {'message': 'Invalid entertainment type ID'}, 404

            place_category = PlaceCategory.query.get(data['category_id'])
            if not place_category:
                return {'message': 'Invalid category ID'}, 404

            default_price_ = data['default_price'] if 'default_price' in data else None

            new_place = Place(
                name=data['name'],
                location = location_,
                latitude = latitude_,
                longitude = longitude_,
                rating=data['rating'],
                entertainment_type_id=data['entertainment_type_id'],
                category_id=data['category_id'],
                default_price = default_price_,
                images=data['images'],
                description=data['description']
            )
            db.session.add(new_place)
            db.session.commit()
            return {'message': 'Place created successfully', 'data': {'id': new_place.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating place: %s', str(e))
            return {'message': 'Failed to create place. Please check inputs and try again.'}, 500


class PlaceResource(Resource):
    @api.marshal_with(place_dto, envelope='data')
    def get(self, place_id):
        """Fetch a specific place"""
        try:
            place = Place.query.get_or_404(place_id)
            return place, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching place: %s', str(e))
            return {'message': 'Failed to fetch place. Please try again.'}, 500

    @jwt_required()
    @api.expect(create_place_dto, validate=True)
    def put(self, place_id):
        """Update a specific place"""
        data = api.payload
        try:
            if 'rating' in data and not (1.0 <= data['rating'] <= 5.0):
                return {'message': 'Rating must be between 1.0 and 5.0'}, 400

            if 'entertainment_type_id' in data:
                entertainment_type = EntertainmentType.query.get(data['entertainment_type_id'])
                if not entertainment_type:
                    return {'message': 'Invalid entertainment type ID'}, 404

            if 'category_id' in data:
                place_category = PlaceCategory.query.get(data['category_id'])
                if not place_category:
                    return {'message': 'Invalid category ID'}, 404

            place = Place.query.get_or_404(place_id)
            if 'name' in data:
                place.name = data['name']
            if 'location' in data:
                place.location = data['location']
            if 'latitude' in data:
                place.latitude = data['latitude']
            if 'longitude' in data:
                place.longitude = data['longitude']
            if 'rating' in data:
                place.rating = data['rating']
            if 'entertainment_type_id' in data:
                place.entertainment_type_id = data['entertainment_type_id']
            if 'category_id' in data:
                place.category_id = data['category_id']
            if 'defualt_price' in data:
                place.defualt_price = data['defualt_price']
            if 'images' in data:
                place.images = data['images']
            if 'description' in data:
                place.description = data['description']
            
            db.session.commit()
            return {'message': 'Place updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating place: %s', str(e))
            return {'message': 'Failed to update place. Please check inputs and try again.'}, 500

    @jwt_required()
    def delete(self, place_id):
        """Delete a specific place"""
        try:
            place = Place.query.get_or_404(place_id)
            db.session.delete(place)
            db.session.commit()
            return {'message': 'Place deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting place: %s', str(e))
            return {'message': 'Failed to delete place. Please try again.'}, 500
