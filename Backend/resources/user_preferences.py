from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, UserPreference
from utils import log_user_activity

class UserPreferencesResource(Resource):
    @log_user_activity('view_user_preferences')
    @jwt_required()
    def get(self):
        try:
            preferences = UserPreference.query.all()
            result = [{'id': preference.id, 'user_id': preference.user_id, 'preference_key': preference.preference_key, 'preference_value': preference.preference_value} for preference in preferences]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user preferences: %s', str(e))
            return {'message': 'Error fetching preferences. Please try again.'}, 500

    @log_user_activity('create_user_preference')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, help='user_id cannot be blank')
        parser.add_argument('preference_key', required=True, help='preference_key cannot be blank')
        parser.add_argument('preference_value', required=True, help='preference_value cannot be blank')
        args = parser.parse_args()

        try:
            new_preference = UserPreference(
                user_id=args['user_id'],
                preference_key=args['preference_key'],
                preference_value=args['preference_value']
            )
            db.session.add(new_preference)
            db.session.commit()
            return {'message': 'User preference created successfully', 'data': {'id': new_preference.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating user preference: %s', str(e))
            return {'message': 'Failed to create user preference. Please try again.'}, 500

class UserPreferenceResource(Resource):
    @jwt_required()
    def get(self, preference_id):
        try:
            preference = UserPreference.query.get_or_404(preference_id)
            result = {
                'id': preference.id,
                'user_id': preference.user_id,
                'preference_key': preference.preference_key,
                'preference_value': preference.preference_value
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user preference: %s', str(e))
            return {'message': 'Error fetching preference. Please try again.'}, 500

    @jwt_required()
    def put(self, preference_id):
        parser = reqparse.RequestParser()
        parser.add_argument('preference_key', type=str)
        parser.add_argument('preference_value', type=str)
        args = parser.parse_args()

        try:
            preference = UserPreference.query.get_or_404(preference_id)
            if 'preference_key' in args:
                preference.preference_key = args['preference_key']
            if 'preference_value' in args:
                preference.preference_value = args['preference_value']
            db.session.commit()
            return {'message': 'User preference updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating user preference: %s', str(e))
            return {'message': 'Failed to update user preference. Please try again.'}, 500

    @jwt_required()
    def delete(self, preference_id):
        try:
            preference = UserPreference.query.get_or_404(preference_id)
            db.session.delete(preference)
            db.session.commit()
            return {'message': 'User preference deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting user preference: %s', str(e))
            return {'message': 'Failed to delete user preference. Please try again.'}, 500
