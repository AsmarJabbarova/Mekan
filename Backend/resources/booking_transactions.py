from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from models import db, BookingTransaction
from utils import log_user_activity

# Namespace
api = Namespace('booking_transactions', description='Operations related to booking transactions')

# DTO Definitions
booking_transaction_dto = api.model('BookingTransaction', {
    'id': fields.Integer(description='Unique ID of the transaction'),
    'booking_id': fields.Integer(required=True, description='ID of the associated booking'),
    'transaction_date': fields.String(required=True, description='Date of the transaction'),
    'amount': fields.Float(required=True, description='Amount of the transaction'),
    'status': fields.String(required=True, description='Status of the transaction')
})

create_booking_transaction_dto = api.model('CreateBookingTransaction', {
    'booking_id': fields.Integer(required=True, description='ID of the associated booking'),
    'transaction_date': fields.String(required=True, description='Date of the transaction'),
    'amount': fields.Float(required=True, description='Amount of the transaction'),
    'status': fields.String(required=True, description='Status of the transaction')
})

update_booking_transaction_dto = api.model('UpdateBookingTransaction', {
    'amount': fields.Float(description='Amount of the transaction'),
    'status': fields.String(description='Status of the transaction')
})


class BookingTransactionsResource(Resource):
    @log_user_activity('view_booking_transactions')
    @jwt_required()
    @api.marshal_list_with(booking_transaction_dto, envelope='data')
    def get(self):
        """Fetch all booking transactions"""
        try:
            transactions = BookingTransaction.query.all()
            return transactions, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching booking transactions: %s', str(e))
            return {'message': 'Error fetching transactions. Please try again.'}, 500

    @log_user_activity('create_booking_transaction')
    @jwt_required()
    @api.expect(create_booking_transaction_dto, validate=True)
    def post(self):
        """Create a new booking transaction"""
        data = api.payload

        try:
            new_transaction = BookingTransaction(
                booking_id=data['booking_id'],
                transaction_date=data['transaction_date'],
                amount=data['amount'],
                status=data['status']
            )
            db.session.add(new_transaction)
            db.session.commit()
            return {'message': 'Transaction created successfully', 'data': {'id': new_transaction.id}}, 201
        except IntegrityError as e:
            app.logger.error('Integrity error while creating transaction: %s', str(e))
            db.session.rollback()
            return {'message': 'Transaction already exists or invalid data.', 'error': str(e)}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error creating transaction: %s', str(e))
            return {'message': 'Failed to create transaction. Please try again.'}, 500


class BookingTransactionResource(Resource):
    @jwt_required()
    @api.marshal_with(booking_transaction_dto, envelope='data')
    def get(self, transaction_id):
        """Fetch a specific booking transaction"""
        try:
            transaction = BookingTransaction.query.get_or_404(transaction_id)
            return transaction, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching transaction: %s', str(e))
            return {'message': 'Error fetching transaction. Please try again.'}, 500

    @jwt_required()
    @api.expect(update_booking_transaction_dto, validate=True)
    def put(self, transaction_id):
        """Update a specific booking transaction"""
        data = api.payload

        try:
            transaction = BookingTransaction.query.get_or_404(transaction_id)
            if 'amount' in data:
                transaction.amount = data['amount']
            if 'status' in data:
                transaction.status = data['status']
            db.session.commit()
            return {'message': 'Transaction updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating transaction: %s', str(e))
            return {'message': 'Failed to update transaction. Please try again.'}, 500

    @jwt_required()
    def delete(self, transaction_id):
        """Delete a specific booking transaction"""
        try:
            transaction = BookingTransaction.query.get_or_404(transaction_id)
            db.session.delete(transaction)
            db.session.commit()
            return {'message': 'Transaction deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting transaction: %s', str(e))
            return {'message': 'Failed to delete transaction. Please try again.'}, 500
