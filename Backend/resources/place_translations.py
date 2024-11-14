from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, PlaceTranslation
from utils import log_user_activity

class PlaceTranslationsResource(Resource):
    @log_user_activity('view_place_translations')
    @jwt_required()
    def get(self):
        try:
            translations = PlaceTranslation.query.all()
            result = [{'id': translation.id, 'place_id': translation.place_id, 'language_id': translation.language_id, 'title': translation.title, 'description': translation.description} for translation in translations]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching place translations: %s', str(e))
            return {'message': 'Error fetching translations. Please try again.'}, 500

    @log_user_activity('create_place_translation')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('place_id', required=True, help='place_id cannot be blank')
        parser.add_argument('language_id', required=True, help='language_id cannot be blank')
        parser.add_argument('title', required=True, help='title cannot be blank')
        parser.add_argument('description', required=True, help='description cannot be blank')
        args = parser.parse_args()

        try:
            new_translation = PlaceTranslation(
                place_id=args['place_id'],
                language_id=args['language_id'],
                title=args['title'],
                description=args['description']
            )
            db.session.add(new_translation)
            db.session.commit()
            return {'message': 'Translation created successfully', 'data': {'id': new_translation.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating translation: %s', str(e))
            return {'message': 'Failed to create translation. Please try again.'}, 500

class PlaceTranslationResource(Resource):
    @jwt_required()
    def get(self, translation_id):
        try:
            translation = PlaceTranslation.query.get_or_404(translation_id)
            result = {
                'id': translation.id,
                'place_id': translation.place_id,
                'language_id': translation.language_id,
                'title': translation.title,
                'description': translation.description
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching translation: %s', str(e))
            return {'message': 'Error fetching translation. Please try again.'}, 500

    @jwt_required()
    def put(self, translation_id):
        parser = reqparse.RequestParser()
        parser.add_argument('title', type=str)
        parser.add_argument('description', type=str)
        args = parser.parse_args()

        try:
            translation = PlaceTranslation.query.get_or_404(translation_id)
            if 'title' in args:
                translation.title = args['title']
            if 'description' in args:
                translation.description = args['description']
            db.session.commit()
            return {'message': 'Translation updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating translation: %s', str(e))
            return {'message': 'Failed to update translation. Please try again.'}, 500

    @jwt_required()
    def delete(self, translation_id):
        try:
            translation = PlaceTranslation.query.get_or_404(translation_id)
            db.session.delete(translation)
            db.session.commit()
            return {'message': 'Translation deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting translation: %s', str(e))
            return {'message': 'Failed to delete translation. Please try again.'}, 500
