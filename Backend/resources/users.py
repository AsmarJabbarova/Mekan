from flask_restful import Resource, reqparse
from models import db, User

class UsersResource(Resource):
    def get(self):
        users = User.query.all()
        return {'data': [user.to_dict() for user in users]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True)
        parser.add_argument('email', required=True)
        parser.add_argument('password', required=True)
        args = parser.parse_args()

        new_user = User(
            username=args['username'],
            email=args['email'],
            password=args['password']
        )
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201
