from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Company
from utils import log_user_activity

class CompaniesResource(Resource):
    @log_user_activity('view_companies')
    @jwt_required()
    def get(self):
        try:
            companies = Company.query.all()
            result = [{'id': company.id, 'name': company.name} for company in companies]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching companies: %s', str(e))
            return {'message': 'Error fetching companies. Please try again later.'}, 500

    @log_user_activity('create_company')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name cannot be blank')
        args = parser.parse_args()

        if Company.query.filter_by(name=args['name']).first():
            return {'message': 'Company with this name already exists.'}, 400

        if len(args['name']) < 3 or len(args['name']) > 100:
            return {'message': 'Company name must be between 3 and 100 characters.'}, 400
        
        try:
            new_company = Company(name=args['name'])
            db.session.add(new_company)
            db.session.commit()
            return {'message': 'Company created successfully', 'data': {'id': new_company.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating company: %s', str(e))
            return {'message': 'Failed to create company. Please try again later.'}, 500

class CompanyResource(Resource):
    @jwt_required()
    def get(self, company_id):
        try:
            company = Company.query.get_or_404(company_id)
            result = {'id': company.id, 'name': company.name}
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching company: %s', str(e))
            return {'message': 'Failed to fetch company. Please try again later.'}, 500

    @jwt_required()
    def put(self, company_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()

        if 'name' in args and (len(args['name']) < 3 or len(args['name']) > 100):
            return {'message': 'Company name must be between 3 and 100 characters.'}, 400

        if 'name' in args and Company.query.filter_by(name=args['name']).first():
            return {'message': 'Company with this name already exists.'}, 400
        
        try:
            company = Company.query.get_or_404(company_id)
            if 'name' in args:
                company.name = args['name']
            db.session.commit()
            return {'message': 'Company updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating company: %s', str(e))
            return {'message': 'Failed to update company. Please try again later.'}, 500

    @jwt_required()
    def delete(self, company_id):
        try:
            company = Company.query.get_or_404(company_id)
            db.session.delete(company)
            db.session.commit()
            return {'message': 'Company deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting company: %s', str(e))
            return {'message': 'Failed to delete company. Please try again later.'}, 500
