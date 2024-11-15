from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from models import db, PlaceTranslation
from utils import log_user_activity

# Namespace
api = Namespace('place_translations', description='Operations related to place translations')

# DTO Definitions
place_translation_dto = api.model('PlaceTranslation', {
    'id': fields.Integer(description='Unique ID of the translation'),
    'place_id': fields.Integer(required=True, description='ID of the associated place'),
    'language_id': fields.Integer(required=True, description='ID of the language'),
    'title': fields.String(required=True, description='Translated title of the place'),
    'description': fields.String(required=True, description='Translated description of the place')
})

create_place_translation_dto = api.model('CreatePlaceTranslation', {
    'place_id': fields.Integer(required=True, description='ID of the associated place'),
    'language_id': fields.Integer(required=True, description='ID of the language'),
    'title': fields.String(required=True, description='Translated title of the place'),
    'description': fields.String(required=True, description='Translated description of the place')
})

update_place_translation_dto = api.model('UpdatePlaceTranslation', {
    'title': fields.String(description='Updated translated title of the place'),
    'description': fields.String(description='Updated translated description of the place')
})


class PlaceTranslationsResource(Resource):
    @log_user_activity('view_place_translations')
    @jwt_required()
    @api.marshal_list_with(place_translation_dto, envelope='data')
    def get(self):
        """Fetch all place translations"""
        try:
            translations = PlaceTranslation.query.all()
            return translations, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching place translations: %s', str(e))
            return {'message': 'Error fetching translations. Please try again.'}, 500

    @log_user_activity('create_place_translation')
    @jwt_required()
    @api.expect(create_place_translation_dto, validate=True)
    def post(self):
        """Create a new place translation"""
        data = api.payload

        try:
            new_translation = PlaceTranslation(
                place_id=data['place_id'],
                language_id=data['language_id'],
                title=data['title'],
                description=data['description']
            )
            db.session.add(new_translation)
            db.session.commit()
            return {'message': 'Translation created successfully', 'data': {'id': new_translation.id}}, 201
        except IntegrityError as e:
            app.logger.error('Integrity error while creating translation: %s', str(e))
            db.session.rollback()
            return {'message': 'Invalid data or translation already exists. Please check place_id and language_id.', 'error': str(e)}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error creating translation: %s', str(e))
            return {'message': 'Failed to create translation. Please try again.'}, 500


class PlaceTranslationResource(Resource):
    @jwt_required()
    @api.marshal_with(place_translation_dto, envelope='data')
    def get(self, translation_id):
        """Fetch a specific place translation"""
        try:
            translation = PlaceTranslation.query.get_or_404(translation_id)
            return translation, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching translation: %s', str(e))
            return {'message': 'Error fetching translation. Please try again.'}, 500

    @jwt_required()
    @api.expect(update_place_translation_dto, validate=True)
    def put(self, translation_id):
        """Update a specific place translation"""
        data = api.payload

        try:
            translation = PlaceTranslation.query.get_or_404(translation_id)
            translation.title = data.get('title', translation.title)
            translation.description = data.get('description', translation.description)

            db.session.commit()
            return {'message': 'Translation updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating translation: %s', str(e))
            return {'message': 'Failed to update translation. Please try again.'}, 500

    @jwt_required()
    def delete(self, translation_id):
        """Delete a specific place translation"""
        try:
            translation = PlaceTranslation.query.get_or_404(translation_id)
            db.session.delete(translation)
            db.session.commit()
            return {'message': 'Translation deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting translation: %s', str(e))
            return {'message': 'Failed to delete translation. Please try again.'}, 500
