from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from models import db, Company
from utils import log_user_activity

# Namespace
api = Namespace('companies', description='Operations related to companies')

# DTO Definitions
company_dto = api.model('Company', {
    'id': fields.Integer(description='Unique ID of the company'),
    'name': fields.String(required=True, description='Name of the company')
})

create_company_dto = api.model('CreateCompany', {
    'name': fields.String(required=True, description='Name of the company (3-100 characters)')
})

update_company_dto = api.model('UpdateCompany', {
    'name': fields.String(description='Name of the company (3-100 characters)')
})


class CompaniesResource(Resource):
    @log_user_activity('view_companies')
    @jwt_required()
    @api.marshal_list_with(company_dto, envelope='data')
    def get(self):
        """Fetch all companies"""
        try:
            companies = Company.query.all()
            return companies, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching companies: %s', str(e))
            return {'message': 'Error fetching companies. Please try again later.'}, 500

    @log_user_activity('create_company')
    @jwt_required()
    @api.expect(create_company_dto, validate=True)
    def post(self):
        """Create a new company"""
        data = api.payload

        if len(data['name']) < 3 or len(data['name']) > 100:
            return {'message': 'Company name must be between 3 and 100 characters.'}, 400

        if Company.query.filter_by(name=data['name']).first():
            return {'message': 'Company with this name already exists.'}, 400

        try:
            new_company = Company(name=data['name'])
            db.session.add(new_company)
            db.session.commit()
            return {'message': 'Company created successfully', 'data': {'id': new_company.id}}, 201
        except IntegrityError as e:
            app.logger.error('Integrity error while creating company: %s', str(e))
            db.session.rollback()
            return {'message': 'Failed to create company. Name might already exist.'}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error creating company: %s', str(e))
            return {'message': 'Failed to create company. Please try again later.'}, 500


class CompanyResource(Resource):
    @jwt_required()
    @api.marshal_with(company_dto, envelope='data')
    def get(self, company_id):
        """Fetch a specific company"""
        try:
            company = Company.query.get_or_404(company_id)
            return company, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching company: %s', str(e))
            return {'message': 'Failed to fetch company. Please try again later.'}, 500

    @jwt_required()
    @api.expect(update_company_dto, validate=True)
    def put(self, company_id):
        """Update a specific company"""
        data = api.payload

        if 'name' in data and (len(data['name']) < 3 or len(data['name']) > 100):
            return {'message': 'Company name must be between 3 and 100 characters.'}, 400

        if 'name' in data and Company.query.filter_by(name=data['name']).first():
            return {'message': 'Company with this name already exists.'}, 400

        try:
            company = Company.query.get_or_404(company_id)
            if 'name' in data:
                company.name = data['name']
            db.session.commit()
            return {'message': 'Company updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating company: %s', str(e))
            return {'message': 'Failed to update company. Please try again later.'}, 500

    @jwt_required()
    def delete(self, company_id):
        """Delete a specific company"""
        try:
            company = Company.query.get_or_404(company_id)
            db.session.delete(company)
            db.session.commit()
            return {'message': 'Company deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting company: %s', str(e))
            return {'message': 'Failed to delete company. Please try again later.'}, 500
