from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, ReviewMedia
from utils import log_user_activity

class ReviewMediasResource(Resource):
    @log_user_activity('view_review_medias')
    @jwt_required()
    def get(self):
        try:
            medias = ReviewMedia.query.all()
            result = [{'id': media.id, 'review_id': media.review_id, 'media_type': media.media_type, 'media_url': media.media_url} for media in medias]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching review medias: %s', str(e))
            return {'message': 'Error fetching medias. Please try again.'}, 500

    @log_user_activity('create_review_media')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('review_id', required=True, help='review_id cannot be blank')
        parser.add_argument('media_type', required=True, help='media_type cannot be blank')
        parser.add_argument('media_url', required=True, help='media_url cannot be blank')
        args = parser.parse_args()

        try:
            new_media = ReviewMedia(
                review_id=args['review_id'],
                media_type=args['media_type'],
                media_url=args['media_url']
            )
            db.session.add(new_media)
            db.session.commit()
            return {'message': 'Review media created successfully', 'data': {'id': new_media.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating review media: %s', str(e))
            return {'message': 'Failed to create review media. Please try again.'}, 500

class ReviewMediaResource(Resource):
    @jwt_required()
    def get(self, media_id):
        try:
            media = ReviewMedia.query.get_or_404(media_id)
            result = {
                'id': media.id,
                'review_id': media.review_id,
                'media_type': media.media_type,
                'media_url': media.media_url
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching review media: %s', str(e))
            return {'message': 'Error fetching media. Please try again.'}, 500

    @jwt_required()
    def put(self, media_id):
        parser = reqparse.RequestParser()
        parser.add_argument('media_type', type=str)
        parser.add_argument('media_url', type=str)
        args = parser.parse_args()

        try:
            media = ReviewMedia.query.get_or_404(media_id)
            if 'media_type' in args:
                media.media_type = args['media_type']
            if 'media_url' in args:
                media.media_url = args['media_url']
            db.session.commit()
            return {'message': 'Review media updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating review media: %s', str(e))
            return {'message': 'Failed to update review media. Please try again.'}, 500

    @jwt_required()
    def delete(self, media_id):
        try:
            media = ReviewMedia.query.get_or_404(media_id)
            db.session.delete(media)
            db.session.commit()
            return {'message': 'Review media deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting review media: %s', str(e))
            return {'message': 'Failed to delete review media. Please try again.'}, 500
