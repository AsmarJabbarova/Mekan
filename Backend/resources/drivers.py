from flask import current_app as app, jsonify
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Driver
from utils import log_user_activity

def validate_age(age):
    if not (18 <= age <= 100):
        return {'message': 'Age must be between 18 and 100.'}, 400
    return None

class DriversResource(Resource):
    @log_user_activity('view_drivers')
    @jwt_required()
    def get(self):
        try:
            drivers = Driver.query.all()
            result = [{'id': driver.id, 'company_id': driver.company_id, 'name': driver.name, 'surname': driver.surname, 'age': driver.age, 'language_id': driver.language_id, 'status': driver.status} for driver in drivers]
            return jsonify({'data': result}), 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching drivers: %s', str(e))
            return {'message': 'Error fetching drivers. Please try again later.'}, 500

    @log_user_activity('create_driver')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('company_id', required=True, help='company_id cannot be blank')
        parser.add_argument('name', required=True, help='name cannot be blank')
        parser.add_argument('surname', required=True, help='surname cannot be blank')
        parser.add_argument('age', required=True, type=int, help='age cannot be blank')
        parser.add_argument('language_id', required=True, help='language_id cannot be blank')
        parser.add_argument('status', required=True, help='status cannot be blank')
        args = parser.parse_args()

        if Driver.query.filter_by(name=args['name'], company_id=args['company_id']).first():
            return {'message': 'Driver with this name already exists in the specified company.'}, 400

        age_validation = validate_age(args['age'])
        if age_validation:
            return age_validation
        
        try:
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
            return {'message': 'Driver created successfully', 'data': {'id': new_driver.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating driver: %s', str(e))
            return {'message': 'Failed to create driver. Please try again later.'}, 500

class DriverResource(Resource):
    @jwt_required()
    def get(self, driver_id):
        try:
            driver = Driver.query.get_or_404(driver_id)
            result = {
                'id': driver.id,
                'company_id': driver.company_id,
                'name': driver.name,
                'surname': driver.surname,
                'age': driver.age,
                'language_id': driver.language_id,
                'status': driver.status
            }
            return jsonify({'data': result}), 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching driver: %s', str(e))
            return {'message': 'Failed to fetch driver. Please try again later.'}, 500

    @jwt_required()
    def put(self, driver_id):
        parser = reqparse.RequestParser()
        parser.add_argument('company_id', type=int)
        parser.add_argument('name', type=str)
        parser.add_argument('surname', type=str)
        parser.add_argument('age', type=int)
        parser.add_argument('language_id', type=int)
        parser.add_argument('status', type=str)
        args = parser.parse_args()

        if args.get('age'):
            age_validation = validate_age(args['age'])
            if age_validation:
                return age_validation

        try:
            driver = Driver.query.get_or_404(driver_id)
            if 'company_id' in args:
                driver.company_id = args['company_id']
            if 'name' in args:
                driver.name = args['name']
            if 'surname' in args:
                driver.surname = args['surname']
            if 'age' in args:
                driver.age = args['age']
            if 'language_id' in args:
                driver.language_id = args['language_id']
            if 'status' in args:
                driver.status = args['status']
            db.session.commit()
            return {'message': 'Driver updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating driver: %s', str(e))
            return {'message': 'Failed to update driver. Please try again later.'}, 500

    @jwt_required()
    def delete(self, driver_id):
        try:
            driver = Driver.query.get_or_404(driver_id)
            db.session.delete(driver)
            db.session.commit()
            return {'message': 'Driver deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting driver: %s', str(e))
            return {'message': 'Failed to delete driver. Please try again later.'}, 500
