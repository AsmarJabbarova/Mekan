from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from models import db, Review, Place, User
from utils import log_user_activity
from datetime import datetime

# Namespace
api = Namespace('reviews', description='Operations related to reviews')

# DTO Definitions
review_dto = api.model('Review', {
    'id': fields.Integer(description='Unique ID of the review'),
    'place_id': fields.Integer(required=True, description='ID of the place being reviewed'),
    'user_id': fields.Integer(required=True, description='ID of the user who posted the review'),
    'rating': fields.Float(required=True, description='Rating of the place (1-5)'),
    'comment': fields.String(required=True, description='User comment on the place'),
    'publish_date': fields.DateTime(description='Date and time the review was published')
})

create_review_dto = api.model('CreateReview', {
    'place_id': fields.Integer(required=True, description='ID of the place being reviewed'),
    'user_id': fields.Integer(required=True, description='ID of the user who posts the review'),
    'rating': fields.Float(required=True, description='Rating of the place (1-5)'),
    'comment': fields.String(required=True, description='User comment about the place')
})


class ReviewsResource(Resource):
    @log_user_activity('view_reviews')
    @jwt_required()
    @api.marshal_list_with(review_dto, envelope='data')
    def get(self):
        """Fetch all reviews"""
        try:
            reviews = Review.query.all()
            return reviews, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching reviews: %s', str(e))
            return {'message': 'Error fetching reviews'}, 500

    @log_user_activity('create_review')
    @jwt_required()
    @api.expect(create_review_dto, validate=True)
    def post(self):
        """Create a new review"""
        data = api.payload

        if not (1 <= data['rating'] <= 5):
            return {'message': 'Rating must be between 1 and 5'}, 400

        place = Place.query.get(data['place_id'])
        if not place:
            return {'message': 'Place not found'}, 404

        user = User.query.get(data['user_id'])
        if not user:
            return {'message': 'User not found'}, 404

        try:
            new_review = Review(
                place_id=data['place_id'],
                user_id=data['user_id'],
                rating=data['rating'],
                comment=data['comment'],
                publish_date=data.get('publish_date', datetime.utcnow())
            )
            db.session.add(new_review)
            db.session.commit()
            return {'message': 'Review created successfully', 'data': {'id': new_review.id}}, 201
        except IntegrityError as e:
            app.logger.error('Integrity error creating review: %s', str(e))
            db.session.rollback()
            return {'message': 'Invalid data, check place_id or user_id'}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error creating review: %s', str(e))
            return {'message': 'Error creating review'}, 500


class ReviewResource(Resource):
    @jwt_required()
    @api.marshal_with(review_dto, envelope='data')
    def get(self, review_id):
        """Fetch a specific review"""
        try:
            review = Review.query.get_or_404(review_id)
            return review, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching review: %s', str(e))
            return {'message': 'Error fetching review'}, 500

    @jwt_required()
    @api.expect(create_review_dto, validate=False)
    def put(self, review_id):
        """Update a specific review"""
        data = api.payload

        if 'rating' in data and not (1 <= data['rating'] <= 5):
            return {'message': 'Rating must be between 1 and 5'}, 400

        try:
            review = Review.query.get_or_404(review_id)

            if 'rating' in data:
                review.rating = data['rating']
            if 'comment' in data:
                review.comment = data['comment']

            db.session.commit()
            return {'message': 'Review updated successfully'}, 200
        except IntegrityError as e:
            app.logger.error('Integrity error updating review: %s', str(e))
            db.session.rollback()
            return {'message': 'Invalid data provided'}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error updating review: %s', str(e))
            return {'message': 'Error updating review'}, 500

    @jwt_required()
    def delete(self, review_id):
        """Delete a specific review"""
        try:
            review = Review.query.get_or_404(review_id)
            db.session.delete(review)
            db.session.commit()
            return {'message': 'Review deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting review: %s', str(e))
            return {'message': 'Error deleting review'}, 500
