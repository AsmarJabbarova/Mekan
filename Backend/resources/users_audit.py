from flask_restful import Resource, reqparse
from models import db, UsersAudit

class UsersAuditResource(Resource):
    def get(self):
        audits = UsersAudit.query.all()
        return {'data': [audit.to_dict() for audit in audits]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True)
        parser.add_argument('action', required=True)
        parser.add_argument('changed_data', required=True)
        args = parser.parse_args()

        new_audit = UsersAudit(
            user_id=args['user_id'],
            action=args['action'],
            changed_data=args['changed_data']
        )
        db.session.add(new_audit)
        db.session.commit()
        return {'message': 'Audit created successfully'}, 201
