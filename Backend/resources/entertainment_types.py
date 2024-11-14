from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, EntertainmentType
from utils import log_user_activity

class EntertainmentTypesResource(Resource):
    @log_user_activity('view_entertainment_types')
    @jwt_required()
    def get(self):
        try:
            types = EntertainmentType.query.all()
            result = [{'id': etype.id, 'name': etype.name} for etype in types]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching entertainment types: %s', str(e))
            return {'message': 'Error fetching entertainment types. Please try again.'}, 500

    @log_user_activity('create_entertainment_type')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name cannot be blank')
        args = parser.parse_args()

        if EntertainmentType.query.filter_by(name=args['name']).first():
            return {'message': 'Entertainment type with this name already exists.'}, 400
        
        try:
            new_type = EntertainmentType(name=args['name'])
            db.session.add(new_type)
            db.session.commit()
            return {'message': 'Entertainment type created successfully', 'data': {'id': new_type.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating entertainment type: %s', str(e))
            return {'message': 'Error creating entertainment type. Please check inputs and try again.'}, 500

class EntertainmentTypeResource(Resource):
    @jwt_required()
    def get(self, etype_id):
        try:
            etype = EntertainmentType.query.get_or_404(etype_id)
            result = {'id': etype.id, 'name': etype.name}
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching entertainment type: %s', str(e))
            return {'message': 'Error fetching entertainment type. Please try again.'}, 500

    @jwt_required()
    def put(self, etype_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()

        if args['name']:
            existing_type = EntertainmentType.query.filter_by(name=args['name']).first()
            if existing_type:
                return {'message': 'Entertainment type with this name already exists.'}, 400

        try:
            etype = EntertainmentType.query.get_or_404(etype_id)
            if args['name']:
                etype.name = args['name']
            db.session.commit()
            return {'message': 'Entertainment type updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating entertainment type: %s', str(e))
            return {'message': 'Error updating entertainment type. Please check inputs and try again.'}, 500

    @jwt_required()
    def delete(self, etype_id):
        try:
            etype = EntertainmentType.query.get_or_404(etype_id)
            db.session.delete(etype)
            db.session.commit()
            return {'message': 'Entertainment type deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting entertainment type: %s', str(e))
            return {'message': 'Error deleting entertainment type. Please try again.'}, 500
