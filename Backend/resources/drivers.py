from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from models import db, Driver
from utils import log_user_activity

# Namespace
api = Namespace('drivers', description='Operations related to drivers')

# DTO Definitions
driver_dto = api.model('Driver', {
    'id': fields.Integer(description='Unique ID of the driver'),
    'company_id': fields.Integer(required=True, description='Company ID associated with the driver'),
    'name': fields.String(required=True, description='First name of the driver'),
    'surname': fields.String(required=True, description='Last name of the driver'),
    'age': fields.Integer(required=True, description='Age of the driver'),
    'language_id': fields.Integer(required=True, description='Language ID for the driver'),
    'status': fields.String(required=True, description='Status of the driver (active/inactive)')
})

create_driver_dto = api.model('CreateDriver', {
    'company_id': fields.Integer(required=True, description='Company ID associated with the driver'),
    'name': fields.String(required=True, description='First name of the driver'),
    'surname': fields.String(required=True, description='Last name of the driver'),
    'age': fields.Integer(required=True, description='Age of the driver (18-100)'),
    'language_id': fields.Integer(required=True, description='Language ID for the driver'),
    'status': fields.String(required=True, description='Status of the driver (active/inactive)')
})

update_driver_dto = api.model('UpdateDriver', {
    'company_id': fields.Integer(description='Company ID associated with the driver'),
    'name': fields.String(description='First name of the driver'),
    'surname': fields.String(description='Last name of the driver'),
    'age': fields.Integer(description='Age of the driver (18-100)'),
    'language_id': fields.Integer(description='Language ID for the driver'),
    'status': fields.String(description='Status of the driver (active/inactive)')
})

def validate_age(age):
    if not (18 <= age <= 100):
        return {'message': 'Age must be between 18 and 100.'}, 400
    return None


class DriversResource(Resource):
    @log_user_activity('view_drivers')
    @jwt_required()
    @api.marshal_list_with(driver_dto, envelope='data')
    def get(self):
        """Fetch all drivers"""
        try:
            drivers = Driver.query.all()
            return drivers, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching drivers: %s', str(e))
            return {'message': 'Error fetching drivers. Please try again later.'}, 500

    @log_user_activity('create_driver')
    @jwt_required()
    @api.expect(create_driver_dto, validate=True)
    def post(self):
        """Create a new driver"""
        data = api.payload

        age_validation = validate_age(data['age'])
        if age_validation:
            return age_validation

        if Driver.query.filter_by(name=data['name'], company_id=data['company_id']).first():
            return {'message': 'Driver with this name already exists in the specified company.'}, 400

        try:
            new_driver = Driver(
                company_id=data['company_id'],
                name=data['name'],
                surname=data['surname'],
                age=data['age'],
                language_id=data['language_id'],
                status=data['status']
            )
            db.session.add(new_driver)
            db.session.commit()
            return {'message': 'Driver created successfully', 'data': {'id': new_driver.id}}, 201
        except IntegrityError as e:
            app.logger.error('Integrity error while creating driver: %s', str(e))
            db.session.rollback()
            return {'message': 'Failed to create driver. Please check input data.'}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error creating driver: %s', str(e))
            return {'message': 'Failed to create driver. Please try again later.'}, 500


class DriverResource(Resource):
    @jwt_required()
    @api.marshal_with(driver_dto, envelope='data')
    def get(self, driver_id):
        """Fetch a specific driver"""
        try:
            driver = Driver.query.get_or_404(driver_id)
            return driver, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching driver: %s', str(e))
            return {'message': 'Failed to fetch driver. Please try again later.'}, 500

    @jwt_required()
    @api.expect(update_driver_dto, validate=True)
    def put(self, driver_id):
        """Update a specific driver"""
        data = api.payload

        if 'age' in data:
            age_validation = validate_age(data['age'])
            if age_validation:
                return age_validation

        try:
            driver = Driver.query.get_or_404(driver_id)

            if 'company_id' in data:
                driver.company_id = data['company_id']
            if 'name' in data:
                driver.name = data['name']
            if 'surname' in data:
                driver.surname = data['surname']
            if 'age' in data:
                driver.age = data['age']
            if 'language_id' in data:
                driver.language_id = data['language_id']
            if 'status' in data:
                driver.status = data['status']

            db.session.commit()
            return {'message': 'Driver updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating driver: %s', str(e))
            return {'message': 'Failed to update driver. Please try again later.'}, 500

    @jwt_required()
    def delete(self, driver_id):
        """Delete a specific driver"""
        try:
            driver = Driver.query.get_or_404(driver_id)
            db.session.delete(driver)
            db.session.commit()
            return {'message': 'Driver deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting driver: %s', str(e))
            return {'message': 'Failed to delete driver. Please try again later.'}, 500
