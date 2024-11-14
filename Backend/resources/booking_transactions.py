from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, BookingTransaction
from utils import log_user_activity

class BookingTransactionsResource(Resource):
    @log_user_activity('view_booking_transactions')
    @jwt_required()
    def get(self):
        try:
            transactions = BookingTransaction.query.all()
            result = [{'id': transaction.id, 'booking_id': transaction.booking_id, 'transaction_date': transaction.transaction_date, 'amount': transaction.amount, 'status': transaction.status} for transaction in transactions]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching booking transactions: %s', str(e))
            return {'message': 'Error fetching transactions. Please try again.'}, 500

    @log_user_activity('create_booking_transaction')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('booking_id', required=True, help='booking_id cannot be blank')
        parser.add_argument('transaction_date', required=True, help='transaction_date cannot be blank')
        parser.add_argument('amount', required=True, type=float, help='amount cannot be blank')
        parser.add_argument('status', required=True, help='status cannot be blank')
        args = parser.parse_args()

        try:
            new_transaction = BookingTransaction(
                booking_id=args['booking_id'],
                transaction_date=args['transaction_date'],
                amount=args['amount'],
                status=args['status']
            )
            db.session.add(new_transaction)
            db.session.commit()
            return {'message': 'Transaction created successfully'}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating transaction: %s', str(e))
            return {'message': 'Failed to create transaction. Please try again.'}, 500

class BookingTransactionResource(Resource):
    @jwt_required()
    def get(self, transaction_id):
        try:
            transaction = BookingTransaction.query.get_or_404(transaction_id)
            result = {
                'id': transaction.id,
                'booking_id': transaction.booking_id,
                'transaction_date': transaction.transaction_date,
                'amount': transaction.amount,
                'status': transaction.status
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching transaction: %s', str(e))
            return {'message': 'Error fetching transaction. Please try again.'}, 500

    @jwt_required()
    def put(self, transaction_id):
        parser = reqparse.RequestParser()
        parser.add_argument('amount', type=float)
        parser.add_argument('status', type=str)
        args = parser.parse_args()

        try:
            transaction = BookingTransaction.query.get_or_404(transaction_id)
            if 'amount' in args:
                transaction.amount = args['amount']
            if 'status' in args:
                transaction.status = args['status']
            db.session.commit()
            return {'message': 'Transaction updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating transaction: %s', str(e))
            return {'message': 'Failed to update transaction. Please try again.'}, 500

    @jwt_required()
    def delete(self, transaction_id):
        try:
            transaction = BookingTransaction.query.get_or_404(transaction_id)
            db.session.delete(transaction)
            db.session.commit()
            return {'message': 'Transaction deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting transaction: %s', str(e))
            return {'message': 'Failed to delete transaction. Please try again.'}, 500
