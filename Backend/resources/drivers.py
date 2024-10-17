from flask_restful import Resource, reqparse
from models import db, Driver

class DriversResource(Resource):
    def get(self):
        drivers = Driver.query.all()
        return {'data': [driver.to_dict() for driver in drivers]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('company_id', required=True)
        parser.add_argument('name', required=True)
        parser.add_argument('surname', required=True)
        parser.add_argument('age', required=True)
        parser.add_argument('language_id', required=True)
        parser.add_argument('status', required=True)
        args = parser.parse_args()

        new_driver = Driver(
            company_id=args['company_id'],
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            language_id=args['language_id'],
            status=args['status']
        )
        db.session.add(new_driver)
        db.session.commit()
        return {'message': 'Driver created successfully'}, 201
