from flask import request, current_app as app
from flask_restx import Resource
from sqlalchemy.exc import SQLAlchemyError
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required
from models import db, User
from utils import log_user_activity

class UserLogin(Resource):
    @log_user_activity('login')
    def post(self):
        try:
            data = request.get_json()
            if not data or 'email' not in data or 'password' not in data:
                return {'message': 'Email and password are required fields.'}, 400

            user = User.query.filter_by(email=data['email']).first()

            if user and check_password_hash(user.password_hash, data['password'] + user.password_salt):
                if user.status == 'suspended':
                    return {'message': 'Your account is suspended. Please contact support.'}, 403

                user.last_online = db.func.now()
                db.session.commit()

                access_token = create_access_token(identity=user.id)

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
                        'preferred_location': user.preferences.preferred_location if user.preferences else None
                    } if user.preferences else None,
                    'access_token': access_token
                }
                return result, 200
            else:
                return {'message': 'Invalid email or password'}, 401
        except SQLAlchemyError as e:
            app.logger.error('Error logging in user: %s', str(e))
            return {'message': 'An error occurred during login.'}, 500

class UserLogout(Resource):
    @log_user_activity('logout')
    @jwt_required()
    def post(self):
        try:
            return {'message': 'User logged out successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error logging out user: %s', str(e))
            return {'message': 'An error occurred during logout.'}, 500
