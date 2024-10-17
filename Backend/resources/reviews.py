from flask_restful import Resource, reqparse
from models import db, Review

class ReviewsResource(Resource):
    def get(self):
        reviews = Review.query.all()
        return {'data': [review.to_dict() for review in reviews]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('place_id', required=True)
        parser.add_argument('user_id', required=True)
        parser.add_argument('rating', required=True)
        parser.add_argument('comment', required=True)
        args = parser.parse_args()

        new_review = Review(
            place_id=args['place_id'],
            user_id=args['user_id'],
            rating=args['rating'],
            comment=args['comment']
        )
        db.session.add(new_review)
        db.session.commit()
        return {'message': 'Review created successfully'}, 201
