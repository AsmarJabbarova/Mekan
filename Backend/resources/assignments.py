from flask_restful import Resource, reqparse
from models import db, Assignment

class AssignmentsResource(Resource):
    def get(self):
        assignments = Assignment.query.all()
        return {'data': [assignment.to_dict() for assignment in assignments]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('driver_id', required=True)
        parser.add_argument('place_id', required=True)
        parser.add_argument('assigned_at', required=True)
        args = parser.parse_args()

        new_assignment = Assignment(
            driver_id=args['driver_id'],
            place_id=args['place_id'],
            assigned_at=args['assigned_at']
        )
        db.session.add(new_assignment)
        db.session.commit()
        return {'message': 'Assignment created successfully'}, 201
