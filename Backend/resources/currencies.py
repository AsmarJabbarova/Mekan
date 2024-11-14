from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Currency
from utils import log_user_activity

class CurrenciesResource(Resource):
    @log_user_activity('view_currencies')
    @jwt_required()
    def get(self):
        try:
            currencies = Currency.query.all()
            result = [{'id': currency.id, 'name': currency.name, 'symbol': currency.symbol} for currency in currencies]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching currencies: %s', str(e))
            return {'message': 'Error fetching currencies. Please try again.'}, 500

    @log_user_activity('create_currency')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name cannot be blank')
        parser.add_argument('symbol', required=True, help='Symbol cannot be blank')
        args = parser.parse_args()

        existing_currency = Currency.query.filter_by(name=args['name']).first()
        if existing_currency:
            return {'message': 'Currency already exists'}, 400

        try:
            new_currency = Currency(name=args['name'], symbol=args['symbol'])
            db.session.add(new_currency)
            db.session.commit()
            return {'message': 'Currency created successfully', 'data': {'id': new_currency.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating currency: %s', str(e))
            return {'message': 'Failed to create currency. Please try again.'}, 500

class CurrencyResource(Resource):
    @jwt_required()
    def get(self, currency_id):
        try:
            currency = Currency.query.get_or_404(currency_id)
            result = {'id': currency.id, 'name': currency.name, 'symbol': currency.symbol}
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching currency: %s', str(e))
            return {'message': 'Error fetching currency. Please try again.'}, 500

    @jwt_required()
    def put(self, currency_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('symbol', type=str)
        args = parser.parse_args()

        try:
            currency = Currency.query.get_or_404(currency_id)
            if 'name' in args:
                currency.name = args['name']
            if 'symbol' in args:
                currency.symbol = args['symbol']
            db.session.commit()
            return {'message': 'Currency updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating currency: %s', str(e))
            return {'message': 'Failed to update currency. Please try again.'}, 500

    @jwt_required()
    def delete(self, currency_id):
        try:
            currency = Currency.query.get_or_404(currency_id)
            db.session.delete(currency)
            db.session.commit()
            return {'message': 'Currency deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting currency: %s', str(e))
            return {'message': 'Failed to delete currency. Please try again.'}, 500
