from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, UserAudit, User
from utils import log_user_activity

class UsersAuditResource(Resource):
    @log_user_activity('fetch_audits')
    @jwt_required()
    def get(self):
        try:
            audits = UserAudit.query.all()
            result = [{
                'id': audit.id,
                'user_id': audit.user_id,
                'action': audit.action,
                'changed_data': audit.changed_data,
                'action_timestamp': audit.action_timestamp.isoformat()
            } for audit in audits]
            return result, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching user audits: %s', str(e))
            return {'message': str(e)}, 500
    
    @log_user_activity('create_audit')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, type=int, help='user_id cannot be blank')
        parser.add_argument('action', required=True, type=str, help='action cannot be blank')
        parser.add_argument('changed_data', required=True, type=str, help='changed_data cannot be blank')
        args = parser.parse_args()

        try:
            user = User.query.get(args['user_id'])
            if not user:
                return {'message': 'Invalid user_id'}, 404

            new_audit = UserAudit(
                user_id=args['user_id'],
                action=args['action'],
                changed_data=args['changed_data']
            )
            db.session.add(new_audit)
            db.session.commit()
            return {'message': 'Audit created successfully'}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating audit: %s', str(e))
            return {'message': str(e)}, 500
