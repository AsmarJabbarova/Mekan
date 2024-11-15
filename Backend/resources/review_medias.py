from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, ReviewMedia
from utils import log_user_activity

# Namespace
api = Namespace('review_medias', description='Operations related to review media')

# DTO Definitions
review_media_model = api.model('ReviewMedia', {
    'id': fields.Integer(description='The unique identifier of the review media', readonly=True),
    'review_id': fields.Integer(required=True, description='The ID of the associated review'),
    'media_type': fields.String(required=True, description='The type of the media (e.g., image, video)'),
    'media_url': fields.String(required=True, description='The URL of the media'),
})

create_review_media_model = api.model('CreateReviewMedia', {
    'review_id': fields.Integer(required=True, description='The ID of the associated review'),
    'media_type': fields.String(required=True, description='The type of the media'),
    'media_url': fields.String(required=True, description='The URL of the media'),
})


class ReviewMediasResource(Resource):
    @log_user_activity('view_review_medias')
    @jwt_required()
    @api.marshal_with(review_media_model, as_list=True)
    def get(self):
        """Get all review media."""
        try:
            medias = ReviewMedia.query.all()
            return medias, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching review medias: %s', str(e))
            api.abort(500, 'Error fetching review media. Please try again.')

    @log_user_activity('create_review_media')
    @jwt_required()
    @api.expect(create_review_media_model, validate=True)
    @api.marshal_with(review_media_model, code=201)
    def post(self):
        """Create a new review media."""
        data = api.payload
        try:
            new_media = ReviewMedia(
                review_id=data['review_id'],
                media_type=data['media_type'],
                media_url=data['media_url']
            )
            db.session.add(new_media)
            db.session.commit()
            return new_media, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating review media: %s', str(e))
            api.abort(500, 'Failed to create review media. Please try again.')


class ReviewMediaResource(Resource):
    @jwt_required()
    @api.marshal_with(review_media_model)
    def get(self, media_id):
        """Get a specific review media by its ID."""
        try:
            media = ReviewMedia.query.get_or_404(media_id)
            return media, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching review media with ID %s: %s', media_id, str(e))
            api.abort(500, 'Error fetching review media. Please try again.')

    @jwt_required()
    @api.expect(create_review_media_model, validate=True)
    @api.marshal_with(review_media_model)
    def put(self, media_id):
        """Update a review media."""
        data = api.payload
        try:
            media = ReviewMedia.query.get_or_404(media_id)
            media.review_id = data.get('review_id', media.review_id)
            media.media_type = data.get('media_type', media.media_type)
            media.media_url = data.get('media_url', media.media_url)
            db.session.commit()
            return media, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating review media with ID %s: %s', media_id, str(e))
            api.abort(500, 'Failed to update review media. Please try again.')

    @jwt_required()
    def delete(self, media_id):
        """Delete a review media."""
        try:
            media = ReviewMedia.query.get_or_404(media_id)
            db.session.delete(media)
            db.session.commit()
            return {'message': 'Review media deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting review media with ID %s: %s', media_id, str(e))
            api.abort(500, 'Failed to delete review media. Please try again.')
