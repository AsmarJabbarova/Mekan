from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Booking, User, Place
from utils import log_user_activity

class BookingsResource(Resource):
    @log_user_activity('view_bookings')
    @jwt_required()
    def get(self):
        try:
            bookings = Booking.query.all()
            result = [{'id': booking.id, 'user_id': booking.user_id, 'place_id': booking.place_id, 
                       'booking_date': booking.booking_date, 'status': booking.status} for booking in bookings]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching bookings: %s', str(e))
            return {'message': 'Error fetching bookings. Please try again later.'}, 500

    @log_user_activity('create_booking')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, help='user_id cannot be blank')
        parser.add_argument('place_id', required=True, help='place_id cannot be blank')
        parser.add_argument('booking_date', required=True, help='booking_date cannot be blank')
        parser.add_argument('status', required=True, help='status cannot be blank')
        args = parser.parse_args()

        if not User.query.get(args['user_id']):
            return {'message': 'User does not exist.'}, 400
        if not Place.query.get(args['place_id']):
            return {'message': 'Place does not exist.'}, 400
        
        try:
            new_booking = Booking(
                user_id=args['user_id'],
                place_id=args['place_id'],
                booking_date=args['booking_date'],
                status=args['status']
            )
            db.session.add(new_booking)
            db.session.commit()
            return {'message': 'Booking created successfully', 'data': {'id': new_booking.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating booking: %s', str(e))
            return {'message': 'Failed to create booking. Please try again later.'}, 500

class BookingResource(Resource):
    @jwt_required()
    def get(self, booking_id):
        try:
            booking = Booking.query.get_or_404(booking_id)
            result = {
                'id': booking.id,
                'user_id': booking.user_id,
                'place_id': booking.place_id,
                'booking_date': booking.booking_date,
                'status': booking.status
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching booking: %s', str(e))
            return {'message': 'Failed to fetch booking. Please try again later.'}, 500

    @jwt_required()
    def put(self, booking_id):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int)
        parser.add_argument('place_id', type=int)
        parser.add_argument('booking_date', type=str)
        parser.add_argument('status', type=str)
        args = parser.parse_args()

        if 'user_id' in args and not User.query.get(args['user_id']):
            return {'message': 'User does not exist.'}, 400
        if 'place_id' in args and not Place.query.get(args['place_id']):
            return {'message': 'Place does not exist.'}, 400

        try:
            booking = Booking.query.get_or_404(booking_id)
            if 'user_id' in args:
                booking.user_id = args['user_id']
            if 'place_id' in args:
                booking.place_id = args['place_id']
            if 'booking_date' in args:
                booking.booking_date = args['booking_date']
            if 'status' in args:
                booking.status = args['status']
            db.session.commit()
            return {'message': 'Booking updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating booking: %s', str(e))
            return {'message': 'Failed to update booking. Please try again later.'}, 500

    @jwt_required()
    def delete(self, booking_id):
        try:
            booking = Booking.query.get_or_404(booking_id)
            db.session.delete(booking)
            db.session.commit()
            return {'message': 'Booking deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting booking: %s', str(e))
            return {'message': 'Failed to delete booking. Please try again later.'}, 500
