from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Payment
from utils import log_user_activity

# Namespace
api = Namespace('payments', description='Operations related to payments')

# DTO Definitions
payment_dto = api.model('Payment', {
    'id': fields.Integer(description='Unique ID of the payment'),
    'booking_id': fields.Integer(required=True, description='ID of the booking associated with the payment'),
    'amount': fields.Float(required=True, description='Amount of the payment'),
    'payment_date': fields.String(required=True, description='Date of the payment (YYYY-MM-DD format)'),
    'status': fields.String(required=True, description='Status of the payment (e.g., "Paid", "Pending")')
})

create_payment_dto = api.model('CreatePayment', {
    'booking_id': fields.Integer(required=True, description='ID of the booking associated with the payment'),
    'amount': fields.Float(required=True, description='Amount of the payment'),
    'payment_date': fields.String(required=True, description='Date of the payment (YYYY-MM-DD format)'),
    'status': fields.String(required=True, description='Status of the payment (e.g., "Paid", "Pending")')
})

update_payment_dto = api.model('UpdatePayment', {
    'booking_id': fields.Integer(description='Updated ID of the booking'),
    'amount': fields.Float(description='Updated amount of the payment'),
    'payment_date': fields.String(description='Updated date of the payment (YYYY-MM-DD format)'),
    'status': fields.String(description='Updated status of the payment')
})


class PaymentsResource(Resource):
    @log_user_activity('view_payments')
    @jwt_required()
    @api.marshal_list_with(payment_dto, envelope='data')
    def get(self):
        """Fetch all payments"""
        try:
            payments = Payment.query.all()
            return payments, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching payments: %s', str(e))
            return {'message': 'Failed to fetch payments. Please try again later.'}, 500

    @log_user_activity('create_payment')
    @jwt_required()
    @api.expect(create_payment_dto, validate=True)
    def post(self):
        """Create a new payment"""
        data = api.payload

        try:
            new_payment = Payment(
                booking_id=data['booking_id'],
                amount=data['amount'],
                payment_date=data['payment_date'],
                status=data['status']
            )
            db.session.add(new_payment)
            db.session.commit()
            return {'message': 'Payment created successfully', 'data': api.marshal(new_payment, payment_dto)}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating payment: %s', str(e))
            return {'message': 'Failed to create payment. Please check the input and try again.'}, 500


class PaymentResource(Resource):
    @jwt_required()
    @api.marshal_with(payment_dto, envelope='data')
    def get(self, payment_id):
        """Fetch a specific payment by ID"""
        try:
            payment = Payment.query.get_or_404(payment_id)
            return payment, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching payment: %s', str(e))
            return {'message': 'Failed to fetch payment. Please try again later.'}, 500

    @jwt_required()
    @api.expect(update_payment_dto, validate=True)
    def put(self, payment_id):
        """Update a specific payment"""
        data = api.payload

        try:
            payment = Payment.query.get_or_404(payment_id)
            if 'booking_id' in data:
                payment.booking_id = data['booking_id']
            if 'amount' in data:
                payment.amount = data['amount']
            if 'payment_date' in data:
                payment.payment_date = data['payment_date']
            if 'status' in data:
                payment.status = data['status']
            db.session.commit()
            return {'message': 'Payment updated successfully', 'data': api.marshal(payment, payment_dto)}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating payment: %s', str(e))
            return {'message': 'Failed to update payment. Please try again later.'}, 500

    @jwt_required()
    def delete(self, payment_id):
        """Delete a specific payment"""
        try:
            payment = Payment.query.get_or_404(payment_id)
            db.session.delete(payment)
            db.session.commit()
            return {'message': 'Payment deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting payment: %s', str(e))
            return {'message': 'Failed to delete payment. Please try again later.'}, 500
