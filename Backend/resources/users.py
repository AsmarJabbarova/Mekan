from flask import request, current_app as app
from flask_restx import Resource
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required
from models import User, db, UserPreference, UserAudit
from utils import log_user_activity
import os

class UsersResource(Resource):
    @log_user_activity('fetch_users')
    @jwt_required()
    def get(self):
        try:
            users = User.query.all()
            result = [
                {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'status': user.status,
                    'last_online': user.last_online.isoformat() if user.last_online else None,
                    'preferences': {
                        'preferred_entertainment_type': user.preferences.preferred_entertainment_type,
                        'preferred_rating_range': user.preferences.preferred_rating_range,
                        'preferred_language': user.preferences.preferred_language,
                        'preferred_location': user.preferences.preferred_location,
                        'preferred_price_range': user.preferences.preferred_price_range
                    } if user.preferences else None
                } for user in users
            ]
            return result, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching users: %s', str(e))
            return {'message': 'An error occurred while fetching users.'}, 500

    @log_user_activity('create_user')
    def post(self):
        try:
            data = request.get_json()
            if not data.get('username') or not data.get('email') or not data.get('password'):
                return {'message': 'Username, email, and password are required fields.'}, 400

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
    def get(self, user_id):
        try:
            user = User.query.get_or_404(user_id)
            result = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'status': user.status,
                'last_online': user.last_online.isoformat() if user.last_online else None,
                'preferences': {
                    'preferred_entertainment_type': user.preferences.preferred_entertainment_type if user.preferences else None,
                    'preferred_rating_range': user.preferences.preferred_rating_range if user.preferences else None,
                    'preferred_language': user.preferences.preferred_language if user.preferences else None,
                    'preferred_location': user.preferences.preferred_location if user.preferences else None,
                    'preferred_price_range': user.preferences.preferred_price_range if user.preferences else None
                }
            }
            return result, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user: %s', str(e))
            return {'message': 'An error occurred while fetching the user.'}, 500

    @jwt_required()
    def put(self, user_id):
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
            if 'last_online' in data:
                user.last_online = data['last_online'].isoformat()

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
        try:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()

            audit = UserAudit(
                user_id=user.id,
                action='deleted user',
                changed_data=None
            )
            db.session.add(audit)
            db.session.commit()

            return {'message': 'User deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting user: %s', str(e))
            return {'message': 'An error occurred while deleting the user.'}, 500
