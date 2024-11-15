from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, PricingRule
from utils import log_user_activity

# Namespace
api = Namespace('pricing_rules', description='Operations related to pricing rules')

# DTO Definitions
pricing_rule_dto = api.model('PricingRule', {
    'id': fields.Integer(description='Unique ID of the pricing rule'),
    'place_id': fields.Integer(required=True, description='ID of the associated place'),
    'currency_id': fields.Integer(required=True, description='ID of the currency used'),
    'price': fields.Float(required=True, description='Price value for the rule'),
    'start_date': fields.String(required=True, description='Start date of the pricing rule'),
    'end_date': fields.String(required=True, description='End date of the pricing rule')
})

create_pricing_rule_dto = api.model('CreatePricingRule', {
    'place_id': fields.Integer(required=True, description='ID of the associated place'),
    'currency_id': fields.Integer(required=True, description='ID of the currency used'),
    'price': fields.Float(required=True, description='Price value for the rule'),
    'start_date': fields.String(required=True, description='Start date of the pricing rule'),
    'end_date': fields.String(required=True, description='End date of the pricing rule')
})

def format_pricing_rule(rule):
    """Helper function to format a PricingRule object into a dictionary."""
    return {
        'id': rule.id,
        'place_id': rule.place_id,
        'currency_id': rule.currency_id,
        'price': rule.price,
        'start_date': rule.start_date,
        'end_date': rule.end_date
    }


class PricingRulesResource(Resource):
    @log_user_activity('view_pricing_rules')
    @jwt_required()
    @api.marshal_list_with(pricing_rule_dto, envelope='data')
    def get(self):
        """Fetch all pricing rules."""
        try:
            rules = PricingRule.query.all()
            return rules, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching pricing rules: %s', str(e))
            return {'message': 'Error fetching rules. Please try again.'}, 500

    @log_user_activity('create_pricing_rule')
    @jwt_required()
    @api.expect(create_pricing_rule_dto, validate=True)
    def post(self):
        """Create a new pricing rule."""
        data = api.payload

        try:
            new_rule = PricingRule(
                place_id=data['place_id'],
                currency_id=data['currency_id'],
                price=data['price'],
                start_date=data['start_date'],
                end_date=data['end_date']
            )
            db.session.add(new_rule)
            db.session.commit()
            return {'message': 'Pricing rule created successfully', 'data': format_pricing_rule(new_rule)}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating pricing rule: %s', str(e))
            return {'message': 'Failed to create pricing rule. Please try again.'}, 500


class PricingRuleResource(Resource):
    @log_user_activity('view_pricing_rule')
    @jwt_required()
    @api.marshal_with(pricing_rule_dto, envelope='data')
    def get(self, rule_id):
        """Fetch a specific pricing rule by ID."""
        try:
            rule = PricingRule.query.get_or_404(rule_id)
            return rule, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching pricing rule: %s', str(e))
            return {'message': 'Error fetching rule. Please try again.'}, 500

    @log_user_activity('update_pricing_rule')
    @jwt_required()
    @api.expect(create_pricing_rule_dto, validate=False)
    def put(self, rule_id):
        """Update a pricing rule by ID."""
        data = api.payload

        try:
            rule = PricingRule.query.get_or_404(rule_id)
            if 'place_id' in data:
                rule.place_id = data['place_id']
            if 'currency_id' in data:
                rule.currency_id = data['currency_id']
            if 'price' in data:
                rule.price = data['price']
            if 'start_date' in data:
                rule.start_date = data['start_date']
            if 'end_date' in data:
                rule.end_date = data['end_date']

            db.session.commit()
            return {'message': 'Pricing rule updated successfully', 'data': format_pricing_rule(rule)}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating pricing rule: %s', str(e))
            return {'message': 'Failed to update pricing rule. Please try again.'}, 500

    @log_user_activity('delete_pricing_rule')
    @jwt_required()
    def delete(self, rule_id):
        """Delete a pricing rule by ID."""
        try:
            rule = PricingRule.query.get_or_404(rule_id)
            db.session.delete(rule)
            db.session.commit()
            return {'message': 'Pricing rule deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting pricing rule: %s', str(e))
            return {'message': 'Failed to delete pricing rule. Please try again.'}, 500
