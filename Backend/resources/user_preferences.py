from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, UserPreference
from utils import log_user_activity

# Namespace
api = Namespace('user_preferences', description='Operations related to user preferences')

# DTO Definitions
user_preference_model = api.model('UserPreference', {
    'id': fields.Integer(description='The unique identifier of the user preference', readonly=True),
    'user_id': fields.Integer(required=True, description='The ID of the user'),
    'preference_key': fields.String(required=True, description='The key of the user preference'),
    'preference_value': fields.String(required=True, description='The value of the user preference'),
})

create_user_preference_model = api.model('CreateUserPreference', {
    'user_id': fields.Integer(required=True, description='The ID of the user'),
    'preference_key': fields.String(required=True, description='The key of the user preference'),
    'preference_value': fields.String(required=True, description='The value of the user preference'),
})


class UserPreferencesResource(Resource):
    @log_user_activity('view_user_preferences')
    @jwt_required()
    @api.marshal_with(user_preference_model, as_list=True)
    def get(self):
        """Get all user preferences."""
        try:
            preferences = UserPreference.query.all()
            return preferences, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user preferences: %s', str(e))
            api.abort(500, 'Error fetching preferences. Please try again.')

    @log_user_activity('create_user_preference')
    @jwt_required()
    @api.expect(create_user_preference_model, validate=True)
    @api.marshal_with(user_preference_model, code=201)
    def post(self):
        """Create a new user preference."""
        data = api.payload
        try:
            new_preference = UserPreference(
                user_id=data['user_id'],
                preference_key=data['preference_key'],
                preference_value=data['preference_value']
            )
            db.session.add(new_preference)
            db.session.commit()
            return new_preference, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating user preference: %s', str(e))
            api.abort(500, 'Failed to create user preference. Please try again.')


class UserPreferenceResource(Resource):
    @jwt_required()
    @api.marshal_with(user_preference_model)
    def get(self, preference_id):
        """Get a specific user preference by its ID."""
        try:
            preference = UserPreference.query.get_or_404(preference_id)
            return preference, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user preference with ID %s: %s', preference_id, str(e))
            api.abort(500, 'Error fetching preference. Please try again.')

    @jwt_required()
    @api.expect(create_user_preference_model, validate=True)
    @api.marshal_with(user_preference_model)
    def put(self, preference_id):
        """Update a user preference."""
        data = api.payload
        try:
            preference = UserPreference.query.get_or_404(preference_id)
            preference.preference_key = data.get('preference_key', preference.preference_key)
            preference.preference_value = data.get('preference_value', preference.preference_value)
            db.session.commit()
            return preference, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating user preference with ID %s: %s', preference_id, str(e))
            api.abort(500, 'Failed to update user preference. Please try again.')

    @jwt_required()
    def delete(self, preference_id):
        """Delete a user preference."""
        try:
            preference = UserPreference.query.get_or_404(preference_id)
            db.session.delete(preference)
            db.session.commit()
            return {'message': 'User preference deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting user preference with ID %s: %s', preference_id, str(e))
            api.abort(500, 'Failed to delete user preference. Please try again.')
