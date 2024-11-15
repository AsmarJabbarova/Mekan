from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from models import db, Currency
from utils import log_user_activity

# Namespace
api = Namespace('currencies', description='Operations related to currencies')

# DTO Definitions
currency_dto = api.model('Currency', {
    'id': fields.Integer(description='Unique ID of the currency'),
    'name': fields.String(required=True, description='Name of the currency'),
    'symbol': fields.String(required=True, description='Symbol of the currency')
})

create_currency_dto = api.model('CreateCurrency', {
    'name': fields.String(required=True, description='Name of the currency (unique)'),
    'symbol': fields.String(required=True, description='Symbol of the currency')
})

update_currency_dto = api.model('UpdateCurrency', {
    'name': fields.String(description='Updated name of the currency'),
    'symbol': fields.String(description='Updated symbol of the currency')
})


class CurrenciesResource(Resource):
    @log_user_activity('view_currencies')
    @jwt_required()
    @api.marshal_list_with(currency_dto, envelope='data')
    def get(self):
        """Fetch all currencies"""
        try:
            currencies = Currency.query.all()
            return currencies, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching currencies: %s', str(e))
            return {'message': 'Error fetching currencies. Please try again later.'}, 500

    @log_user_activity('create_currency')
    @jwt_required()
    @api.expect(create_currency_dto, validate=True)
    def post(self):
        """Create a new currency"""
        data = api.payload

        if Currency.query.filter_by(name=data['name']).first():
            return {'message': 'Currency with this name already exists.'}, 400

        try:
            new_currency = Currency(name=data['name'], symbol=data['symbol'])
            db.session.add(new_currency)
            db.session.commit()
            return {'message': 'Currency created successfully', 'data': {'id': new_currency.id}}, 201
        except IntegrityError as e:
            app.logger.error('Integrity error while creating currency: %s', str(e))
            db.session.rollback()
            return {'message': 'Failed to create currency. Name or symbol might already exist.'}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error creating currency: %s', str(e))
            return {'message': 'Failed to create currency. Please try again later.'}, 500


class CurrencyResource(Resource):
    @jwt_required()
    @api.marshal_with(currency_dto, envelope='data')
    def get(self, currency_id):
        """Fetch a specific currency"""
        try:
            currency = Currency.query.get_or_404(currency_id)
            return currency, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching currency: %s', str(e))
            return {'message': 'Error fetching currency. Please try again later.'}, 500

    @jwt_required()
    @api.expect(update_currency_dto, validate=True)
    def put(self, currency_id):
        """Update a specific currency"""
        data = api.payload

        try:
            currency = Currency.query.get_or_404(currency_id)

            if 'name' in data:
                if Currency.query.filter_by(name=data['name']).first():
                    return {'message': 'Currency with this name already exists.'}, 400
                currency.name = data['name']
            
            if 'symbol' in data:
                currency.symbol = data['symbol']

            db.session.commit()
            return {'message': 'Currency updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating currency: %s', str(e))
            return {'message': 'Failed to update currency. Please try again later.'}, 500

    @jwt_required()
    def delete(self, currency_id):
        """Delete a specific currency"""
        try:
            currency = Currency.query.get_or_404(currency_id)
            db.session.delete(currency)
            db.session.commit()
            return {'message': 'Currency deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting currency: %s', str(e))
            return {'message': 'Failed to delete currency. Please try again later.'}, 500
