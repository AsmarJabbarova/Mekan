from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from models import db, Booking, User, Place
from utils import log_user_activity

# Namespace
api = Namespace('bookings', description='Operations related to bookings')

# DTO Definitions
booking_dto = api.model('Booking', {
    'id': fields.Integer(description='Unique ID of the booking'),
    'user_id': fields.Integer(required=True, description='ID of the user making the booking'),
    'place_id': fields.Integer(required=True, description='ID of the place being booked'),
    'total_cost': fields.Float(required=True, description='Total cost of the booking'),
    'booking_date': fields.String(required=True, description='Date of the booking'),
    'status': fields.String(required=True, description='Status of the booking')
})

create_booking_dto = api.model('CreateBooking', {
    'user_id': fields.Integer(required=True, description='ID of the user making the booking'),
    'place_id': fields.Integer(required=True, description='ID of the place being booked'),
    'total_cost': fields.Float(required=True, description='Total cost of the booking'),
    'booking_date': fields.String(required=True, description='Date of the booking'),
    'status': fields.String(required=True, description='Status of the booking')
})

update_booking_dto = api.model('UpdateBooking', {
    'user_id': fields.Integer(description='ID of the user making the booking'),
    'place_id': fields.Integer(description='ID of the place being booked'),
    'booking_date': fields.String(description='Date of the booking'),
    'status': fields.String(description='Status of the booking')
})


class BookingsResource(Resource):
    @log_user_activity('view_bookings')
    @jwt_required()
    @api.marshal_list_with(booking_dto, envelope='data')
    def get(self):
        """Fetch all bookings"""
        try:
            bookings = Booking.query.all()
            return bookings, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching bookings: %s', str(e))
            return {'message': 'Error fetching bookings. Please try again later.'}, 500

    @log_user_activity('create_booking')
    @jwt_required()
    @api.expect(create_booking_dto, validate=True)
    def post(self):
        """Create a new booking"""
        data = api.payload

        if not User.query.get(data['user_id']):
            return {'message': 'User does not exist.'}, 400
        if not Place.query.get(data['place_id']):
            return {'message': 'Place does not exist.'}, 400

        try:
            new_booking = Booking(
                user_id=data['user_id'],
                place_id=data['place_id'],
                booking_date=data['booking_date'],
                status=data['status'],
                total_cost=data['total_cost']
            )
            db.session.add(new_booking)
            db.session.commit()
            return {'message': 'Booking created successfully', 'data': {'id': new_booking.id}}, 201
        except IntegrityError as e:
            app.logger.error('Integrity error while creating booking: %s', str(e))
            db.session.rollback()
            return {'message': 'Booking already exists or invalid data.', 'error': str(e)}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error creating booking: %s', str(e))
            return {'message': 'Failed to create booking. Please try again later.'}, 500


class BookingResource(Resource):
    @jwt_required()
    @api.marshal_with(booking_dto, envelope='data')
    def get(self, booking_id):
        """Fetch a specific booking"""
        try:
            booking = Booking.query.get_or_404(booking_id)
            return booking, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching booking: %s', str(e))
            return {'message': 'Failed to fetch booking. Please try again later.'}, 500

    @jwt_required()
    @api.expect(update_booking_dto, validate=True)
    def put(self, booking_id):
        """Update a specific booking"""
        data = api.payload

        if 'user_id' in data and not User.query.get(data['user_id']):
            return {'message': 'User does not exist.'}, 400
        if 'place_id' in data and not Place.query.get(data['place_id']):
            return {'message': 'Place does not exist.'}, 400

        try:
            booking = Booking.query.get_or_404(booking_id)
            if 'user_id' in data:
                booking.user_id = data['user_id']
            if 'place_id' in data:
                booking.place_id = data['place_id']
            if 'booking_date' in data:
                booking.booking_date = data['booking_date']
            if 'status' in data:
                booking.status = data['status']
            db.session.commit()
            return {'message': 'Booking updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating booking: %s', str(e))
            return {'message': 'Failed to update booking. Please try again later.'}, 500

    @jwt_required()
    def delete(self, booking_id):
        """Delete a specific booking"""
        try:
            booking = Booking.query.get_or_404(booking_id)
            db.session.delete(booking)
            db.session.commit()
            return {'message': 'Booking deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting booking: %s', str(e))
            return {'message': 'Failed to delete booking. Please try again later.'}, 500
