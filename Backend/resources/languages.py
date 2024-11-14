from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Language
from utils import log_user_activity

def check_existing_language(name):
    return Language.query.filter_by(name=name).first()

class LanguagesResource(Resource):
    @log_user_activity('view_languages')
    @jwt_required()
    def get(self):
        try:
            languages = Language.query.all()
            result = [{'id': lang.id, 'name': lang.name} for lang in languages]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching languages: %s', str(e))
            return {'message': 'Error fetching languages. Please try again later.'}, 500

    @log_user_activity('create_language')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name cannot be blank')
        args = parser.parse_args()

        existing_language = check_existing_language(args['name'])
        if existing_language:
            return {'message': 'Language already exists'}, 400

        try:
            new_language = Language(name=args['name'])
            db.session.add(new_language)
            db.session.commit()
            return {'message': 'Language created successfully', 'data': {'id': new_language.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating language: %s', str(e))
            return {'message': 'Failed to create language. Please check the input and try again.'}, 500

class LanguageResource(Resource):
    @jwt_required()
    def get(self, language_id):
        try:
            language = Language.query.get_or_404(language_id)
            result = {
                'id': language.id,
                'name': language.name
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching language: %s', str(e))
            return {'message': 'Error fetching language. Please try again later.'}, 500

    @jwt_required()
    def put(self, language_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()

        if args['name']:
            existing_language = check_existing_language(args['name'])
            if existing_language:
                return {'message': 'Language with this name already exists'}, 400

        try:
            language = Language.query.get_or_404(language_id)
            if args['name']:
                language.name = args['name']
            db.session.commit()
            return {'message': 'Language updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating language: %s', str(e))
            return {'message': 'Failed to update language. Please try again later.'}, 500

    @jwt_required()
    def delete(self, language_id):
        try:
            language = Language.query.get_or_404(language_id)
            db.session.delete(language)
            db.session.commit()
            return {'message': 'Language deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting language: %s', str(e))
            return {'message': 'Failed to delete language. Please try again later.'}, 500
