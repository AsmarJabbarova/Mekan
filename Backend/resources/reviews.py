from flask import request, current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from models import db, Review, Place, User
from utils import log_user_activity
from datetime import datetime

class ReviewsResource(Resource):
    @log_user_activity('view_reviews')
    @jwt_required()
    def get(self):
        try:
            reviews = Review.query.all()
            result = [
                {
                    'id': review.id,
                    'place_id': review.place_id,
                    'user_id': review.user_id,
                    'rating': review.rating,
                    'comment': review.comment,
                    'publish_date': review.publish_date.isoformat() if review.publish_date else None
                } for review in reviews
            ]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching reviews: %s', str(e))
            return {'message': 'Error fetching reviews', 'error': str(e)}, 500

    @log_user_activity('create_review')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('place_id', type=int, required=True, help='place_id cannot be blank')
        parser.add_argument('user_id', type=int, required=True, help='user_id cannot be blank')
        parser.add_argument('rating', type=float, required=True, help='rating cannot be blank and must be a float')
        parser.add_argument('comment', type=str, required=True, help='comment cannot be blank')
        args = parser.parse_args()

        if not (1 <= args['rating'] <= 5):
            return {'message': 'Rating must be between 1 and 5'}, 400

        place = Place.query.get(args['place_id'])
        if not place:
            return {'message': 'Place not found'}, 404
        
        user = User.query.get(args['user_id'])
        if not user:
            return {'message': 'User not found'}, 404

        try:
            new_review = Review(
                place_id=args['place_id'],
                user_id=args['user_id'],
                rating=args['rating'],
                comment=args['comment'],
                publish_date=request.json.get('publish_date', datetime.utcnow())
            )
            db.session.add(new_review)
            db.session.commit()
            return {'message': 'Review created successfully', 'data': {'id': new_review.id}}, 201
        except IntegrityError as e:
            app.logger.error('Integrity error creating review: %s', str(e))
            db.session.rollback()
            return {'message': 'Invalid data, check place_id or user_id', 'error': str(e)}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error creating review: %s', str(e))
            return {'message': 'Error creating review', 'error': str(e)}, 500

class ReviewResource(Resource):
    @jwt_required()
    def get(self, review_id):
        try:
            review = Review.query.get_or_404(review_id)
            result = {
                'id': review.id,
                'place_id': review.place_id,
                'user_id': review.user_id,
                'rating': review.rating,
                'comment': review.comment,
                'publish_date': review.publish_date.isoformat() if review.publish_date else None
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching review: %s', str(e))
            return {'message': 'Error fetching review', 'error': str(e)}, 500

    @jwt_required()
    def put(self, review_id):
        parser = reqparse.RequestParser()
        parser.add_argument('rating', type=float)
        parser.add_argument('comment', type=str)
        args = parser.parse_args()

        if args['rating'] is not None and not (1 <= args['rating'] <= 5):
            return {'message': 'Rating must be between 1 and 5'}, 400

        try:
            review = Review.query.get_or_404(review_id)
            data = request.get_json()

            review.rating = data.get('rating', review.rating)
            review.comment = data.get('comment', review.comment)

            db.session.commit()
            return {'message': 'Review updated successfully'}, 200
        except IntegrityError as e:
            app.logger.error('Integrity error updating review: %s', str(e))
            db.session.rollback()
            return {'message': 'Invalid data provided', 'error': str(e)}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error updating review: %s', str(e))
            return {'message': 'Error updating review', 'error': str(e)}, 500

    @jwt_required()
    def delete(self, review_id):
        try:
            review = Review.query.get_or_404(review_id)
            db.session.delete(review)
            db.session.commit()
            return {'message': 'Review deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting review: %s', str(e))
            return {'message': 'Error deleting review', 'error': str(e)}, 500
