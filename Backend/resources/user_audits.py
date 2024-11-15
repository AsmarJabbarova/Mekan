from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, UserAudit, User
from utils import log_user_activity

# Namespace
api = Namespace('user_audits', description='User audit related operations')

# DTO Definitions
audit_dto = api.model('UserAudit', {
    'id': fields.Integer(description='Unique ID of the audit log'),
    'user_id': fields.Integer(required=True, description='ID of the user associated with the audit'),
    'action': fields.String(required=True, description='Action performed by the user'),
    'changed_data': fields.String(description='Details of the data that changed'),
    'action_timestamp': fields.DateTime(description='Timestamp of the action')
})

audit_create_dto = api.model('CreateUserAudit', {
    'user_id': fields.Integer(required=True, description='ID of the user associated with the audit'),
    'action': fields.String(required=True, description='Action performed by the user'),
    'changed_data': fields.String(required=True, description='Details of the data that changed')
})


class UserAuditsResource(Resource):
    @log_user_activity('fetch_audits')
    @jwt_required()
    @api.marshal_list_with(audit_dto, envelope='audits')
    def get(self):
        """Fetch all user audits"""
        try:
            audits = UserAudit.query.all()
            return audits, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user audits: %s', str(e))
            return {'message': 'An error occurred while fetching audits.'}, 500

    @log_user_activity('create_audit')
    @jwt_required()
    @api.expect(audit_create_dto, validate=True)
    def post(self):
        """Create a new user audit"""
        try:
            data = api.payload

            user = User.query.get(data['user_id'])
            if not user:
                return {'message': 'Invalid user_id'}, 404

            new_audit = UserAudit(
                user_id=data['user_id'],
                action=data['action'],
                changed_data=data['changed_data']
            )
            db.session.add(new_audit)
            db.session.commit()
            return {'message': 'Audit created successfully'}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating audit: %s', str(e))
            return {'message': 'An error occurred while creating the audit.'}, 500
