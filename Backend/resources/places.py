from flask_restful import Resource, reqparse
from models import db, Place

class PlacesResource(Resource):
    def get(self):
        places = Place.query.all()
        return {'data': [place.to_dict() for place in places]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        parser.add_argument('location', required=True)
        parser.add_argument('rating', required=True)
        parser.add_argument('entertainment_type_id', required=True)
        args = parser.parse_args()

        new_place = Place(
            name=args['name'],
            location=args['location'],
            rating=args['rating'],
            entertainment_type_id=args['entertainment_type_id']
        )
        db.session.add(new_place)
        db.session.commit()
        return {'message': 'Place created successfully'}, 201
