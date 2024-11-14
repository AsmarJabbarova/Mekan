from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Payment
from utils import log_user_activity

def format_payment(payment):
    return {
        'id': payment.id,
        'booking_id': payment.booking_id,
        'amount': payment.amount,
        'payment_date': payment.payment_date,
        'status': payment.status
    }

class PaymentsResource(Resource):
    @log_user_activity('view_payments')
    @jwt_required()
    def get(self):
        try:
            payments = Payment.query.all()
            result = [format_payment(payment) for payment in payments]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching payments: %s', str(e))
            return {'message': 'Failed to fetch payments. Please try again later.'}, 500

    @log_user_activity('create_payment')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('booking_id', required=True, help='booking_id cannot be blank')
        parser.add_argument('amount', type=float, required=True, help='amount cannot be blank')
        parser.add_argument('payment_date', required=True, help='payment_date cannot be blank')
        parser.add_argument('status', required=True, help='status cannot be blank')
        args = parser.parse_args()

        try:
            new_payment = Payment(
                booking_id=args['booking_id'],
                amount=args['amount'],
                payment_date=args['payment_date'],
                status=args['status']
            )
            db.session.add(new_payment)
            db.session.commit()
            return {'message': 'Payment created successfully', 'data': format_payment(new_payment)}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating payment: %s', str(e))
            return {'message': 'Failed to create payment. Please check the input and try again.'}, 500

class PaymentResource(Resource):
    @jwt_required()
    def get(self, payment_id):
        try:
            payment = Payment.query.get_or_404(payment_id)
            return {'data': format_payment(payment)}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching payment: %s', str(e))
            return {'message': 'Failed to fetch payment. Please try again later.'}, 500

    @jwt_required()
    def put(self, payment_id):
        parser = reqparse.RequestParser()
        parser.add_argument('booking_id', type=int)
        parser.add_argument('amount', type=float)
        parser.add_argument('payment_date', type=str)
        parser.add_argument('status', type=str)
        args = parser.parse_args()

        try:
            payment = Payment.query.get_or_404(payment_id)
            if 'booking_id' in args:
                payment.booking_id = args['booking_id']
            if 'amount' in args:
                payment.amount = args['amount']
            if 'payment_date' in args:
                payment.payment_date = args['payment_date']
            if 'status' in args:
                payment.status = args['status']
            db.session.commit()
            return {'message': 'Payment updated successfully', 'data': format_payment(payment)}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating payment: %s', str(e))
            return {'message': 'Failed to update payment. Please try again later.'}, 500

    @jwt_required()
    def delete(self, payment_id):
        try:
            payment = Payment.query.get_or_404(payment_id)
            db.session.delete(payment)
            db.session.commit()
            return {'message': 'Payment deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting payment: %s', str(e))
            return {'message': 'Failed to delete payment. Please try again later.'}, 500
