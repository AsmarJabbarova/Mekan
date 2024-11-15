from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from models import db, Language
from utils import log_user_activity

# Namespace
api = Namespace('languages', description='Operations related to languages')

# DTO Definitions
language_dto = api.model('Language', {
    'id': fields.Integer(description='Unique ID of the language'),
    'name': fields.String(required=True, description='Name of the language')
})

create_language_dto = api.model('CreateLanguage', {
    'name': fields.String(required=True, description='Name of the language')
})

update_language_dto = api.model('UpdateLanguage', {
    'name': fields.String(description='Updated name of the language')
})

def check_existing_language(name):
    """Check if a language with the given name already exists"""
    return Language.query.filter_by(name=name).first()


class LanguagesResource(Resource):
    @log_user_activity('view_languages')
    @jwt_required()
    @api.marshal_list_with(language_dto, envelope='data')
    def get(self):
        """Fetch all languages"""
        try:
            languages = Language.query.all()
            return languages, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching languages: %s', str(e))
            return {'message': 'Error fetching languages. Please try again later.'}, 500

    @log_user_activity('create_language')
    @jwt_required()
    @api.expect(create_language_dto, validate=True)
    def post(self):
        """Create a new language"""
        data = api.payload

        if check_existing_language(data['name']):
            return {'message': 'Language already exists'}, 400

        try:
            new_language = Language(name=data['name'])
            db.session.add(new_language)
            db.session.commit()
            return {'message': 'Language created successfully', 'data': {'id': new_language.id}}, 201
        except IntegrityError as e:
            app.logger.error('Integrity error while creating language: %s', str(e))
            db.session.rollback()
            return {'message': 'Failed to create language. Please check input data.'}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error creating language: %s', str(e))
            return {'message': 'Failed to create language. Please try again later.'}, 500


class LanguageResource(Resource):
    @jwt_required()
    @api.marshal_with(language_dto, envelope='data')
    def get(self, language_id):
        """Fetch a specific language"""
        try:
            language = Language.query.get_or_404(language_id)
            return language, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching language: %s', str(e))
            return {'message': 'Error fetching language. Please try again later.'}, 500

    @jwt_required()
    @api.expect(update_language_dto, validate=True)
    def put(self, language_id):
        """Update a specific language"""
        data = api.payload

        if 'name' in data and check_existing_language(data['name']):
            return {'message': 'Language with this name already exists'}, 400

        try:
            language = Language.query.get_or_404(language_id)

            if 'name' in data:
                language.name = data['name']

            db.session.commit()
            return {'message': 'Language updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating language: %s', str(e))
            return {'message': 'Failed to update language. Please try again later.'}, 500

    @jwt_required()
    def delete(self, language_id):
        """Delete a specific language"""
        try:
            language = Language.query.get_or_404(language_id)
            db.session.delete(language)
            db.session.commit()
            return {'message': 'Language deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting language: %s', str(e))
            return {'message': 'Failed to delete language. Please try again later.'}, 500
