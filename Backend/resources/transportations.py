from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Transportation
from utils import log_user_activity

class TransportationsResource(Resource):
    @log_user_activity('view_transportations')
    @jwt_required()
    def get(self):
        try:
            transportations = Transportation.query.all()
            result = [{'id': transportation.id, 'type': transportation.type, 'capacity': transportation.capacity, 'price': transportation.price} for transportation in transportations]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching transportations: %s', str(e))
            return {'message': 'Error fetching transportations. Please try again.'}, 500

    @log_user_activity('create_transportation')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True, help='Type cannot be blank')
        parser.add_argument('capacity', required=True, type=int, help='Capacity cannot be blank')
        parser.add_argument('price', required=True, type=float, help='Price cannot be blank')
        args = parser.parse_args()

        try:
            new_transportation = Transportation(
                type=args['type'],
                capacity=args['capacity'],
                price=args['price']
            )
            db.session.add(new_transportation)
            db.session.commit()
            return {'message': 'Transportation created successfully', 'data': {'id': new_transportation.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating transportation: %s', str(e))
            return {'message': 'Failed to create transportation. Please try again.'}, 500

class TransportationResource(Resource):
    @jwt_required()
    def get(self, transportation_id):
        try:
            transportation = Transportation.query.get_or_404(transportation_id)
            result = {
                'id': transportation.id,
                'type': transportation.type,
                'capacity': transportation.capacity,
                'price': transportation.price
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching transportation: %s', str(e))
            return {'message': 'Error fetching transportation. Please try again.'}, 500

    @jwt_required()
    def put(self, transportation_id):
        parser = reqparse.RequestParser()
        parser.add_argument('type', type=str)
        parser.add_argument('capacity', type=int)
        parser.add_argument('price', type=float)
        args = parser.parse_args()

        try:
            transportation = Transportation.query.get_or_404(transportation_id)
            if 'type' in args:
                transportation.type = args['type']
            if 'capacity' in args:
                transportation.capacity = args['capacity']
            if 'price' in args:
                transportation.price = args['price']
            db.session.commit()
            return {'message': 'Transportation updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating transportation: %s', str(e))
            return {'message': 'Failed to update transportation. Please try again.'}, 500

    @jwt_required()
    def delete(self, transportation_id):
        try:
            transportation = Transportation.query.get_or_404(transportation_id)
            db.session.delete(transportation)
            db.session.commit()
            return {'message': 'Transportation deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting transportation: %s', str(e))
            return {'message': 'Failed to delete transportation. Please try again.'}, 500
