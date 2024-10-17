from flask_restful import Resource, reqparse
from models import db, Company

class CompaniesResource(Resource):
    def get(self):
        companies = Company.query.all()
        return {'data': [company.to_dict() for company in companies]}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True)
        args = parser.parse_args()

        new_company = Company(name=args['name'])
        db.session.add(new_company)
        db.session.commit()
        return {'message': 'Company created successfully'}, 201
