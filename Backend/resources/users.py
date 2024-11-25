from flask import request, current_app as app
from flask_restx import Resource, fields, Namespace
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required
from models import User, db, UserPreference, UserAudit
from utils import log_user_activity
import os

# Namespace
api = Namespace('users', description='User related operations')

# DTO Definitions
user_preferences_dto = api.model('UserPreferences', {
    'preferred_entertainment_type': fields.String(description='Preferred type of entertainment'),
    'preferred_rating_range': fields.String(description='Preferred rating range'),
    'preferred_language': fields.String(description='Preferred language'),
    'preferred_location': fields.String(description='Preferred location'),
    'preferred_price_range': fields.String(description='Preferred price range')
})

user_dto = api.model('User', {
    'id': fields.Integer(description='Unique ID of the user'),
    'username': fields.String(required=True, description='Username of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'role': fields.String(description='Role of the user'),
    'status': fields.String(description='Status of the user'),
    'last_online': fields.DateTime(description='Last online timestamp'),
    'preferences': fields.Nested(user_preferences_dto, description='User preferences', allow_null=True)
})

user_create_dto = api.model('CreateUser', {
    'username': fields.String(required=True, description='Username of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'role': fields.String(description='Role of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'preferences': fields.Nested(user_preferences_dto, description='User preferences', allow_null=True)
})


class UsersResource(Resource):
    @log_user_activity('fetch_users')
    @jwt_required()
    @api.marshal_list_with(user_dto, envelope='users')
    def get(self):
        """Fetch all users"""
        try:
            users = User.query.all()
            return users, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching users: %s', str(e))
            return {'message': 'An error occurred while fetching users.'}, 500

    @log_user_activity('create_user')
    @api.expect(user_create_dto, validate=True)
    def post(self):
        """Create a new user"""
        try:
            data = request.get_json()

            password_salt = os.urandom(16).hex()
            password_hash = generate_password_hash(data['password'] + password_salt, method='pbkdf2:sha256')

            new_user = User(
                username=data['username'],
                email=data['email'],
                password_salt=password_salt,
                password_hash=password_hash
            )
            db.session.add(new_user)
            db.session.commit()

            if 'preferences' in data:
                preferences_data = data['preferences']
                new_preferences = UserPreference(
                    user_id=new_user.id,
                    preferred_entertainment_type=preferences_data.get('preferred_entertainment_type'),
                    preferred_rating_range=preferences_data.get('preferred_rating_range'),
                    preferred_language=preferences_data.get('preferred_language'),
                    preferred_location=preferences_data.get('preferred_location'),
                    preferred_price_range=preferences_data.get('preferred_price_range')
                )
                db.session.add(new_preferences)
                db.session.commit()

            audit = UserAudit(
                user_id=new_user.id,
                action='created user',
                changed_data=data
            )
            db.session.add(audit)
            db.session.commit()

            return {'message': 'User created successfully'}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating user: %s', str(e))
            return {'message': 'An error occurred while creating the user.'}, 500


class UserResource(Resource):
    @jwt_required()
    @api.marshal_with(user_dto)
    def get(self, user_id):
        """Fetch a user by ID"""
        try:
            user = User.query.get_or_404(user_id)
            return user, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user: %s', str(e))
            return {'message': 'An error occurred while fetching the user.'}, 500

    @jwt_required()
    @api.expect(user_create_dto, validate=True)
    def put(self, user_id):
        """Update a user by ID"""
        try:
            data = request.get_json()
            user = User.query.get_or_404(user_id)

            if 'username' in data:
                user.username = data['username']
            if 'email' in data:
                user.email = data['email']
            if 'password' in data:
                user.password_salt = os.urandom(16).hex()
                user.password_hash = generate_password_hash(data['password'] + user.password_salt, method='pbkdf2:sha256')
            if 'status' in data:
                user.status = data['status']
            if 'preferences' in data:
                preferences_data = data['preferences']
                if user.preferences:
                    user.preferences.preferred_entertainment_type = preferences_data.get('preferred_entertainment_type', user.preferences.preferred_entertainment_type)
                    user.preferences.preferred_rating_range = preferences_data.get('preferred_rating_range', user.preferences.preferred_rating_range)
                    user.preferences.preferred_language = preferences_data.get('preferred_language', user.preferences.preferred_language)
                    user.preferences.preferred_location = preferences_data.get('preferred_location', user.preferences.preferred_location)
                    user.preferences.preferred_price_range = preferences_data.get('preferred_price_range', user.preferences.preferred_price_range)
                else:
                    new_preferences = UserPreference(
                        user_id=user.id,
                        preferred_entertainment_type=preferences_data.get('preferred_entertainment_type'),
                        preferred_rating_range=preferences_data.get('preferred_rating_range'),
                        preferred_language=preferences_data.get('preferred_language'),
                        preferred_location=preferences_data.get('preferred_location'),
                        preferred_price_range=preferences_data.get('preferred_price_range')
                    )
                    db.session.add(new_preferences)

            db.session.commit()

            audit = UserAudit(
                user_id=user.id,
                action='updated user',
                changed_data=data
            )
            db.session.add(audit)
            db.session.commit()

            return {'message': 'User updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating user: %s', str(e))
            return {'message': 'An error occurred while updating the user.'}, 500

    @jwt_required()
    def delete(self, user_id):
        """Delete a user by ID"""
        try:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()

            audit = UserAudit(
                user_id=user.id,
                action='deleted user'
            )
            db.session.add(audit)
            db.session.commit()

            return {'message': 'User deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting user: %s', str(e))
            return {'message': 'An error occurred while deleting the user.'}, 500
