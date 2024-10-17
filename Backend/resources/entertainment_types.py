from flask_restful import Resource, reqparse
from models import db, EntertainmentType

class EntertainmentTypesResource(Resource):
    def get(self):
        types = EntertainmentType.query.all()
        return {'data': [etype.to_dict() for etype in types]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        new_type = EntertainmentType(name=args['name'])
        db.session.add(new_type)
        db.session.commit()
        return {'message': 'Entertainment type created successfully'}, 201
