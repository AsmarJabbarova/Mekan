from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Place, EntertainmentType
from utils import log_user_activity

class PlacesResource(Resource):
    @log_user_activity('view_places')
    @jwt_required()
    def get(self):
        try:
            places = Place.query.all()
            result = [{
                'id': place.id,
                'name': place.name,
                'location': place.location,
                'rating': place.rating,
                'entertainment_type_id': place.entertainment_type_id
            } for place in places]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching places: %s', str(e))
            return {'message': 'Failed to fetch places. Please try again.'}, 500

    @log_user_activity('create_place')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name cannot be blank')
        parser.add_argument('location', required=True, help='Location cannot be blank')
        parser.add_argument('rating', type=float, required=True, help='Rating cannot be blank and must be a number')
        parser.add_argument('entertainment_type_id', type=int, required=True, help='Entertainment Type ID cannot be blank and must be an integer')
        args = parser.parse_args()

        if not (1.0 <= args['rating'] <= 5.0):
            return {'message': 'Rating must be between 1.0 and 5.0'}, 400

        entertainment_type = EntertainmentType.query.get(args['entertainment_type_id'])
        if not entertainment_type:
            return {'message': 'Invalid entertainment type ID'}, 404

        try:
            new_place = Place(
                name=args['name'],
                location=args['location'],
                rating=args['rating'],
                entertainment_type_id=args['entertainment_type_id']
            )
            db.session.add(new_place)
            db.session.commit()
            return {'message': 'Place created successfully', 'data': {'id': new_place.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating place: %s', str(e))
            return {'message': 'Failed to create place. Please check inputs and try again.'}, 500

class PlaceResource(Resource):
    @jwt_required()
    def get(self, place_id):
        try:
            place = Place.query.get_or_404(place_id)
            result = {
                'id': place.id,
                'name': place.name,
                'location': place.location,
                'rating': place.rating,
                'entertainment_type_id': place.entertainment_type_id
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching place: %s', str(e))
            return {'message': 'Failed to fetch place. Please try again.'}, 500

    @jwt_required()
    def put(self, place_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('location', type=str)
        parser.add_argument('rating', type=float)
        parser.add_argument('entertainment_type_id', type=int)
        args = parser.parse_args()

        if args['rating'] and not (1.0 <= args['rating'] <= 5.0):
            return {'message': 'Rating must be between 1.0 and 5.0'}, 400

        if args['entertainment_type_id']:
            entertainment_type = EntertainmentType.query.get(args['entertainment_type_id'])
            if not entertainment_type:
                return {'message': 'Invalid entertainment type ID'}, 404

        try:
            place = Place.query.get_or_404(place_id)
            if args['name']:
                place.name = args['name']
            if args['location']:
                place.location = args['location']
            if args['rating']:
                place.rating = args['rating']
            if args['entertainment_type_id']:
                place.entertainment_type_id = args['entertainment_type_id']
            db.session.commit()
            return {'message': 'Place updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating place: %s', str(e))
            return {'message': 'Failed to update place. Please check inputs and try again.'}, 500

    @jwt_required()
    def delete(self, place_id):
        try:
            place = Place.query.get_or_404(place_id)
            db.session.delete(place)
            db.session.commit()
            return {'message': 'Place deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting place: %s', str(e))
            return {'message': 'Failed to delete place. Please try again.'}, 500
