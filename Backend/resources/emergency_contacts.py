from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, EmergencyContact
from utils import log_user_activity

# Namespace
api = Namespace('emergency_contacts', description='Operations related to emergency contacts')

# DTO Definitions
emergency_contact_dto = api.model('EmergencyContact', {
    'id': fields.Integer(description='Unique ID of the emergency contact'),
    'user_id': fields.Integer(required=True, description='ID of the user associated with this contact'),
    'name': fields.String(required=True, description='Name of the emergency contact'),
    'phone': fields.String(required=True, description='Phone number of the emergency contact'),
    'relation': fields.String(required=True, description='Relation to the user')
})

create_emergency_contact_dto = api.model('CreateEmergencyContact', {
    'user_id': fields.Integer(required=True, description='ID of the user associated with this contact'),
    'name': fields.String(required=True, description='Name of the emergency contact'),
    'phone': fields.String(required=True, description='Phone number of the emergency contact'),
    'relation': fields.String(required=True, description='Relation to the user')
})

update_emergency_contact_dto = api.model('UpdateEmergencyContact', {
    'name': fields.String(description='Updated name of the emergency contact'),
    'phone': fields.String(description='Updated phone number of the emergency contact'),
    'relation': fields.String(description='Updated relation to the user')
})


class EmergencyContactsResource(Resource):
    @log_user_activity('view_emergency_contacts')
    @jwt_required()
    @api.marshal_list_with(emergency_contact_dto, envelope='data')
    def get(self):
        """Fetch all emergency contacts"""
        try:
            contacts = EmergencyContact.query.all()
            return contacts, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching emergency contacts: %s', str(e))
            return {'message': 'Error fetching contacts. Please try again.'}, 500

    @log_user_activity('create_emergency_contact')
    @jwt_required()
    @api.expect(create_emergency_contact_dto, validate=True)
    def post(self):
        """Create a new emergency contact"""
        data = api.payload

        try:
            new_contact = EmergencyContact(
                user_id=data['user_id'],
                name=data['name'],
                phone=data['phone'],
                relation=data['relation']
            )
            db.session.add(new_contact)
            db.session.commit()
            return {'message': 'Emergency contact created successfully', 'data': {'id': new_contact.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating emergency contact: %s', str(e))
            return {'message': 'Failed to create contact. Please try again.'}, 500


class EmergencyContactResource(Resource):
    @jwt_required()
    @api.marshal_with(emergency_contact_dto, envelope='data')
    def get(self, contact_id):
        """Fetch a specific emergency contact"""
        try:
            contact = EmergencyContact.query.get_or_404(contact_id)
            return contact, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching emergency contact: %s', str(e))
            return {'message': 'Error fetching contact. Please try again.'}, 500

    @jwt_required()
    @api.expect(update_emergency_contact_dto, validate=True)
    def put(self, contact_id):
        """Update a specific emergency contact"""
        data = api.payload

        try:
            contact = EmergencyContact.query.get_or_404(contact_id)

            if 'name' in data:
                contact.name = data['name']
            if 'phone' in data:
                contact.phone = data['phone']
            if 'relation' in data:
                contact.relation = data['relation']

            db.session.commit()
            return {'message': 'Emergency contact updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating emergency contact: %s', str(e))
            return {'message': 'Failed to update contact. Please try again.'}, 500

    @jwt_required()
    def delete(self, contact_id):
        """Delete a specific emergency contact"""
        try:
            contact = EmergencyContact.query.get_or_404(contact_id)
            db.session.delete(contact)
            db.session.commit()
            return {'message': 'Emergency contact deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting emergency contact: %s', str(e))
            return {'message': 'Failed to delete contact. Please try again.'}, 500
