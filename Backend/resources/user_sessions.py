from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, UserSession
from utils import log_user_activity

class UserSessionsResource(Resource):
    @log_user_activity('view_user_sessions')
    @jwt_required()
    def get(self):
        try:
            sessions = UserSession.query.all()
            result = [{'id': session.id, 'user_id': session.user_id, 'login_time': session.login_time, 'logout_time': session.logout_time} for session in sessions]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user sessions: %s', str(e))
            return {'message': 'Error fetching sessions. Please try again.'}, 500

    @log_user_activity('create_user_session')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, help='user_id cannot be blank')
        parser.add_argument('login_time', required=True, help='login_time cannot be blank')
        parser.add_argument('logout_time', required=True, help='logout_time cannot be blank')
        args = parser.parse_args()

        try:
            new_session = UserSession(
                user_id=args['user_id'],
                login_time=args['login_time'],
                logout_time=args['logout_time']
            )
            db.session.add(new_session)
            db.session.commit()
            return {'message': 'User session created successfully', 'data': {'id': new_session.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating user session: %s', str(e))
            return {'message': 'Failed to create user session. Please try again.'}, 500

class UserSessionResource(Resource):
    @jwt_required()
    def get(self, session_id):
        try:
            session = UserSession.query.get_or_404(session_id)
            result = {
                'id': session.id,
                'user_id': session.user_id,
                'login_time': session.login_time,
                'logout_time': session.logout_time
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user session: %s', str(e))
            return {'message': 'Error fetching session. Please try again.'}, 500

    @jwt_required()
    def put(self, session_id):
        parser = reqparse.RequestParser()
        parser.add_argument('login_time', type=str)
        parser.add_argument('logout_time', type=str)
        args = parser.parse_args()

        try:
            session = UserSession.query.get_or_404(session_id)
            if 'login_time' in args:
                session.login_time = args['login_time']
            if 'logout_time' in args:
                session.logout_time = args['logout_time']
            db.session.commit()
            return {'message': 'User session updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating user session: %s', str(e))
            return {'message': 'Failed to update user session. Please try again.'}, 500

    @jwt_required()
    def delete(self, session_id):
        try:
            session = UserSession.query.get_or_404(session_id)
            db.session.delete(session)
            db.session.commit()
            return {'message': 'User session deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting user session: %s', str(e))
            return {'message': 'Failed to delete user session. Please try again.'}, 500
