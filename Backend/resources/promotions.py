from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Promotion
from utils import log_user_activity

# Namespace
api = Namespace('promotions', description='Operations related to promotions')

# DTO Definitions
promotion_dto = api.model('Promotion', {
    'id': fields.Integer(description='Unique ID of the promotion'),
    'code': fields.String(required=True, description='Unique code for the promotion'),
    'discount': fields.Float(required=True, description='Discount percentage or value'),
    'valid_from': fields.String(required=True, description='Start date of the promotion'),
    'valid_to': fields.String(required=True, description='End date of the promotion')
})

create_promotion_dto = api.model('CreatePromotion', {
    'code': fields.String(required=True, description='Unique code for the promotion'),
    'discount': fields.Float(required=True, description='Discount percentage or value'),
    'valid_from': fields.String(required=True, description='Start date of the promotion'),
    'valid_to': fields.String(required=True, description='End date of the promotion')
})

def format_promotion(promotion):
    """Helper function to format a Promotion object into a dictionary."""
    return {
        'id': promotion.id,
        'code': promotion.code,
        'discount': promotion.discount,
        'valid_from': promotion.valid_from,
        'valid_to': promotion.valid_to
    }


class PromotionsResource(Resource):
    @log_user_activity('view_promotions')
    @jwt_required()
    @api.marshal_list_with(promotion_dto, envelope='data')
    def get(self):
        """Fetch all promotions."""
        try:
            promotions = Promotion.query.all()
            return promotions, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching promotions: %s', str(e))
            return {'message': 'Error fetching promotions. Please try again.'}, 500

    @log_user_activity('create_promotion')
    @jwt_required()
    @api.expect(create_promotion_dto, validate=True)
    def post(self):
        """Create a new promotion."""
        data = api.payload

        try:
            new_promotion = Promotion(
                code=data['code'],
                discount=data['discount'],
                valid_from=data['valid_from'],
                valid_to=data['valid_to']
            )
            db.session.add(new_promotion)
            db.session.commit()
            return {'message': 'Promotion created successfully', 'data': format_promotion(new_promotion)}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating promotion: %s', str(e))
            return {'message': 'Failed to create promotion. Please try again.'}, 500


class PromotionResource(Resource):
    @log_user_activity('view_promotion')
    @jwt_required()
    @api.marshal_with(promotion_dto, envelope='data')
    def get(self, promo_id):
        """Fetch a specific promotion by ID."""
        try:
            promo = Promotion.query.get_or_404(promo_id)
            return promo, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching promotion: %s', str(e))
            return {'message': 'Error fetching promotion. Please try again.'}, 500

    @log_user_activity('update_promotion')
    @jwt_required()
    @api.expect(create_promotion_dto, validate=False)
    def put(self, promo_id):
        """Update a promotion by ID."""
        data = api.payload

        try:
            promo = Promotion.query.get_or_404(promo_id)
            if 'code' in data:
                promo.code = data['code']
            if 'discount' in data:
                promo.discount = data['discount']
            if 'valid_from' in data:
                promo.valid_from = data['valid_from']
            if 'valid_to' in data:
                promo.valid_to = data['valid_to']
            
            db.session.commit()
            return {'message': 'Promotion updated successfully', 'data': format_promotion(promo)}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating promotion: %s', str(e))
            return {'message': 'Failed to update promotion. Please try again.'}, 500

    @log_user_activity('delete_promotion')
    @jwt_required()
    def delete(self, promo_id):
        """Delete a promotion by ID."""
        try:
            promo = Promotion.query.get_or_404(promo_id)
            db.session.delete(promo)
            db.session.commit()
            return {'message': 'Promotion deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting promotion: %s', str(e))
            return {'message': 'Failed to delete promotion. Please try again.'}, 500
