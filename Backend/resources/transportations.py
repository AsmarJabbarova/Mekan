from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Transportation
from utils import log_user_activity

# Namespace
api = Namespace('transportations', description='Operations related to transportations')

# DTO Definitions
transportation_model = api.model('Transportation', {
    'id': fields.Integer(description='The unique identifier of the transportation', readonly=True),
    'type': fields.String(required=True, description='The type of transportation'),
    'capacity': fields.Integer(required=True, description='The capacity of the transportation'),
    'price': fields.Float(required=True, description='The price of the transportation'),
})

create_transportation_model = api.model('CreateTransportation', {
    'type': fields.String(required=True, description='The type of transportation'),
    'capacity': fields.Integer(required=True, description='The capacity of the transportation'),
    'price': fields.Float(required=True, description='The price of the transportation'),
})


class TransportationsResource(Resource):
    @log_user_activity('view_transportations')
    @jwt_required()
    @api.marshal_with(transportation_model, as_list=True)
    def get(self):
        """Get all transportations."""
        try:
            transportations = Transportation.query.all()
            return transportations, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching transportations: %s', str(e))
            api.abort(500, 'Error fetching transportations. Please try again.')

    @log_user_activity('create_transportation')
    @jwt_required()
    @api.expect(create_transportation_model, validate=True)
    @api.marshal_with(transportation_model, code=201)
    def post(self):
        """Create a new transportation."""
        data = api.payload
        try:
            new_transportation = Transportation(
                type=data['type'],
                capacity=data['capacity'],
                price=data['price']
            )
            db.session.add(new_transportation)
            db.session.commit()
            return new_transportation, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating transportation: %s', str(e))
            api.abort(500, 'Failed to create transportation. Please try again.')


class TransportationResource(Resource):
    @jwt_required()
    @api.marshal_with(transportation_model)
    def get(self, transportation_id):
        """Get a specific transportation by its ID."""
        try:
            transportation = Transportation.query.get_or_404(transportation_id)
            return transportation, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching transportation with ID %s: %s', transportation_id, str(e))
            api.abort(500, 'Error fetching transportation. Please try again.')

    @jwt_required()
    @api.expect(create_transportation_model, validate=True)
    @api.marshal_with(transportation_model)
    def put(self, transportation_id):
        """Update a transportation."""
        data = api.payload
        try:
            transportation = Transportation.query.get_or_404(transportation_id)
            transportation.type = data.get('type', transportation.type)
            transportation.capacity = data.get('capacity', transportation.capacity)
            transportation.price = data.get('price', transportation.price)
            db.session.commit()
            return transportation, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating transportation with ID %s: %s', transportation_id, str(e))
            api.abort(500, 'Failed to update transportation. Please try again.')

    @jwt_required()
    def delete(self, transportation_id):
        """Delete a transportation."""
        try:
            transportation = Transportation.query.get_or_404(transportation_id)
            db.session.delete(transportation)
            db.session.commit()
            return {'message': 'Transportation deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting transportation with ID %s: %s', transportation_id, str(e))
            api.abort(500, 'Failed to delete transportation. Please try again.')
