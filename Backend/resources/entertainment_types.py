from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, EntertainmentType
from utils import log_user_activity

# Namespace
api = Namespace('entertainment_types', description='Operations related to entertainment types')

# DTO Definitions
entertainment_type_dto = api.model('EntertainmentType', {
    'id': fields.Integer(description='Unique ID of the entertainment type'),
    'name': fields.String(required=True, description='Name of the entertainment type')
})

create_entertainment_type_dto = api.model('CreateEntertainmentType', {
    'name': fields.String(required=True, description='Name of the entertainment type')
})


class EntertainmentTypesResource(Resource):
    @log_user_activity('view_entertainment_types')
    @jwt_required()
    @api.marshal_list_with(entertainment_type_dto, envelope='data')
    def get(self):
        """Fetch all entertainment types"""
        try:
            types = EntertainmentType.query.all()
            return types, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching entertainment types: %s', str(e))
            return {'message': 'Error fetching entertainment types. Please try again.'}, 500

    @log_user_activity('create_entertainment_type')
    @jwt_required()
    @api.expect(create_entertainment_type_dto, validate=True)
    def post(self):
        """Create a new entertainment type"""
        data = api.payload
        try:
            if EntertainmentType.query.filter_by(name=data['name']).first():
                return {'message': 'Entertainment type with this name already exists.'}, 400

            new_type = EntertainmentType(name=data['name'])
            db.session.add(new_type)
            db.session.commit()
            return {'message': 'Entertainment type created successfully', 'data': {'id': new_type.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating entertainment type: %s', str(e))
            return {'message': 'Error creating entertainment type. Please check inputs and try again.'}, 500


class EntertainmentTypeResource(Resource):
    @jwt_required()
    @api.marshal_with(entertainment_type_dto, envelope='data')
    def get(self, etype_id):
        """Fetch a specific entertainment type"""
        try:
            etype = EntertainmentType.query.get_or_404(etype_id)
            return etype, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching entertainment type: %s', str(e))
            return {'message': 'Error fetching entertainment type. Please try again.'}, 500

    @jwt_required()
    @api.expect(create_entertainment_type_dto, validate=True)
    def put(self, etype_id):
        """Update an entertainment type"""
        data = api.payload
        try:
            etype = EntertainmentType.query.get_or_404(etype_id)

            if data['name'] and EntertainmentType.query.filter_by(name=data['name']).first():
                return {'message': 'Entertainment type with this name already exists.'}, 400

            etype.name = data['name']
            db.session.commit()
            return {'message': 'Entertainment type updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating entertainment type: %s', str(e))
            return {'message': 'Error updating entertainment type. Please check inputs and try again.'}, 500

    @jwt_required()
    def delete(self, etype_id):
        """Delete an entertainment type"""
        try:
            etype = EntertainmentType.query.get_or_404(etype_id)
            db.session.delete(etype)
            db.session.commit()
            return {'message': 'Entertainment type deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting entertainment type: %s', str(e))
            return {'message': 'Error deleting entertainment type. Please try again.'}, 500
