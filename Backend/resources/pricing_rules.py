from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, PricingRule
from utils import log_user_activity

class PricingRulesResource(Resource):
    @log_user_activity('view_pricing_rules')
    @jwt_required()
    def get(self):
        try:
            rules = PricingRule.query.all()
            result = [{'id': rule.id, 'place_id': rule.place_id, 'currency_id': rule.currency_id, 'price': rule.price, 'start_date': rule.start_date, 'end_date': rule.end_date} for rule in rules]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching pricing rules: %s', str(e))
            return {'message': 'Error fetching rules. Please try again.'}, 500

    @log_user_activity('create_pricing_rule')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('place_id', required=True, help='place_id cannot be blank')
        parser.add_argument('currency_id', required=True, help='currency_id cannot be blank')
        parser.add_argument('price', required=True, type=float, help='price cannot be blank')
        parser.add_argument('start_date', required=True, help='start_date cannot be blank')
        parser.add_argument('end_date', required=True, help='end_date cannot be blank')
        args = parser.parse_args()

        try:
            new_rule = PricingRule(
                place_id=args['place_id'],
                currency_id=args['currency_id'],
                price=args['price'],
                start_date=args['start_date'],
                end_date=args['end_date']
            )
            db.session.add(new_rule)
            db.session.commit()
            return {'message': 'Pricing rule created successfully', 'data': {'id': new_rule.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating pricing rule: %s', str(e))
            return {'message': 'Failed to create pricing rule. Please try again.'}, 500

class PricingRuleResource(Resource):
    @jwt_required()
    def get(self, rule_id):
        try:
            rule = PricingRule.query.get_or_404(rule_id)
            result = {
                'id': rule.id,
                'place_id': rule.place_id,
                'currency_id': rule.currency_id,
                'price': rule.price,
                'start_date': rule.start_date,
                'end_date': rule.end_date
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching pricing rule: %s', str(e))
            return {'message': 'Error fetching rule. Please try again.'}, 500

    @jwt_required()
    def put(self, rule_id):
        parser = reqparse.RequestParser()
        parser.add_argument('place_id', type=int)
        parser.add_argument('currency_id', type=int)
        parser.add_argument('price', type=float)
        parser.add_argument('start_date', type=str)
        parser.add_argument('end_date', type=str)
        args = parser.parse_args()

        try:
            rule = PricingRule.query.get_or_404(rule_id)
            if 'place_id' in args:
                rule.place_id = args['place_id']
            if 'currency_id' in args:
                rule.currency_id = args['currency_id']
            if 'price' in args:
                rule.price = args['price']
            if 'start_date' in args:
                rule.start_date = args['start_date']
            if 'end_date' in args:
                rule.end_date = args['end_date']
            db.session.commit()
            return {'message': 'Pricing rule updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating pricing rule: %s', str(e))
            return {'message': 'Failed to update pricing rule. Please try again.'}, 500

    @jwt_required()
    def delete(self, rule_id):
        try:
            rule = PricingRule.query.get_or_404(rule_id)
            db.session.delete(rule)
            db.session.commit()
            return {'message': 'Pricing rule deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting pricing rule: %s', str(e))
            return {'message': 'Failed to delete pricing rule. Please try again.'}, 500
