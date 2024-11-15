from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, UserSession
from utils import log_user_activity

# Namespace
api = Namespace('user_sessions', description='Operations related to user sessions')

# DTO Definition
user_session_model = api.model('UserSession', {
    'id': fields.Integer(description='The unique identifier of the user session', readonly=True),
    'user_id': fields.Integer(required=True, description='The ID of the user'),
    'login_time': fields.String(required=True, description='The login time of the user'),
    'logout_time': fields.String(required=True, description='The logout time of the user'),
})

create_user_session_model = api.model('CreateUserSession', {
    'user_id': fields.Integer(required=True, description='The ID of the user'),
    'login_time': fields.String(required=True, description='The login time of the user'),
    'logout_time': fields.String(required=True, description='The logout time of the user'),
})


class UserSessionsResource(Resource):
    @log_user_activity('view_user_sessions')
    @jwt_required()
    @api.marshal_with(user_session_model, as_list=True)
    def get(self):
        """Get all user sessions."""
        try:
            sessions = UserSession.query.all()
            return sessions, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user sessions: %s', str(e))
            api.abort(500, 'Error fetching sessions. Please try again.')

    @log_user_activity('create_user_session')
    @jwt_required()
    @api.expect(create_user_session_model, validate=True)
    @api.marshal_with(user_session_model, code=201)
    def post(self):
        """Create a new user session."""
        data = api.payload
        try:
            new_session = UserSession(
                user_id=data['user_id'],
                login_time=data['login_time'],
                logout_time=data['logout_time']
            )
            db.session.add(new_session)
            db.session.commit()
            return new_session, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating user session: %s', str(e))
            api.abort(500, 'Failed to create user session. Please try again.')


class UserSessionResource(Resource):
    @jwt_required()
    @api.marshal_with(user_session_model)
    def get(self, session_id):
        """Get a specific user session by its ID."""
        try:
            session = UserSession.query.get_or_404(session_id)
            return session, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user session with ID %s: %s', session_id, str(e))
            api.abort(500, 'Error fetching session. Please try again.')

    @jwt_required()
    @api.expect(create_user_session_model, validate=True)
    @api.marshal_with(user_session_model)
    def put(self, session_id):
        """Update a user session."""
        data = api.payload
        try:
            session = UserSession.query.get_or_404(session_id)
            session.login_time = data.get('login_time', session.login_time)
            session.logout_time = data.get('logout_time', session.logout_time)
            db.session.commit()
            return session, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating user session with ID %s: %s', session_id, str(e))
            api.abort(500, 'Failed to update user session. Please try again.')

    @jwt_required()
    def delete(self, session_id):
        """Delete a user session."""
        try:
            session = UserSession.query.get_or_404(session_id)
            db.session.delete(session)
            db.session.commit()
            return {'message': 'User session deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting user session with ID %s: %s', session_id, str(e))
            api.abort(500, 'Failed to delete user session. Please try again.')
