from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Promotion
from utils import log_user_activity

class PromotionsResource(Resource):
    @log_user_activity('view_promotions')
    @jwt_required()
    def get(self):
        try:
            promotions = Promotion.query.all()
            result = [{'id': promo.id, 'code': promo.code, 'discount': promo.discount, 'valid_from': promo.valid_from, 'valid_to': promo.valid_to} for promo in promotions]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching promotions: %s', str(e))
            return {'message': 'Error fetching promotions. Please try again.'}, 500

    @log_user_activity('create_promotion')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code', required=True, help='Code cannot be blank')
        parser.add_argument('discount', required=True, type=float, help='Discount cannot be blank')
        parser.add_argument('valid_from', required=True, help='valid_from cannot be blank')
        parser.add_argument('valid_to', required=True, help='valid_to cannot be blank')
        args = parser.parse_args()

        try:
            new_promotion = Promotion(
                code=args['code'],
                discount=args['discount'],
                valid_from=args['valid_from'],
                valid_to=args['valid_to']
            )
            db.session.add(new_promotion)
            db.session.commit()
            return {'message': 'Promotion created successfully', 'data': {'id': new_promotion.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating promotion: %s', str(e))
            return {'message': 'Failed to create promotion. Please try again.'}, 500

class PromotionResource(Resource):
    @jwt_required()
    def get(self, promo_id):
        try:
            promo = Promotion.query.get_or_404(promo_id)
            result = {
                'id': promo.id,
                'code': promo.code,
                'discount': promo.discount,
                'valid_from': promo.valid_from,
                'valid_to': promo.valid_to
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching promotion: %s', str(e))
            return {'message': 'Error fetching promotion. Please try again.'}, 500

    @jwt_required()
    def put(self, promo_id):
        parser = reqparse.RequestParser()
        parser.add_argument('code', type=str)
        parser.add_argument('discount', type=float)
        parser.add_argument('valid_from', type=str)
        parser.add_argument('valid_to', type=str)
        args = parser.parse_args()

        try:
            promo = Promotion.query.get_or_404(promo_id)
            if 'code' in args:
                promo.code = args['code']
            if 'discount' in args:
                promo.discount = args['discount']
            if 'valid_from' in args:
                promo.valid_from = args['valid_from']
            if 'valid_to' in args:
                promo.valid_to = args['valid_to']
            db.session.commit()
            return {'message': 'Promotion updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating promotion: %s', str(e))
            return {'message': 'Failed to update promotion. Please try again.'}, 500

    @jwt_required()
    def delete(self, promo_id):
        try:
            promo = Promotion.query.get_or_404(promo_id)
            db.session.delete(promo)
            db.session.commit()
            return {'message': 'Promotion deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting promotion: %s', str(e))
            return {'message': 'Failed to delete promotion. Please try again.'}, 500
