from flask_restful import Resource, reqparse
from models import db, Language

class LanguagesResource(Resource):
    def get(self):
        languages = Language.query.all()
        return {'data': [language.to_dict() for language in languages]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        new_language = Language(name=args['name'])
        db.session.add(new_language)
        db.session.commit()
        return {'message': 'Language created successfully'}, 201
