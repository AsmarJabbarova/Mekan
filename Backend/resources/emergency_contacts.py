from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, EmergencyContact
from utils import log_user_activity

class EmergencyContactsResource(Resource):
    @log_user_activity('view_emergency_contacts')
    @jwt_required()
    def get(self):
        try:
            contacts = EmergencyContact.query.all()
            result = [{'id': contact.id, 'user_id': contact.user_id, 'name': contact.name, 'phone': contact.phone, 'relation': contact.relation} for contact in contacts]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching emergency contacts: %s', str(e))
            return {'message': 'Error fetching contacts. Please try again.'}, 500

    @log_user_activity('create_emergency_contact')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', required=True, help='user_id cannot be blank')
        parser.add_argument('name', required=True, help='name cannot be blank')
        parser.add_argument('phone', required=True, help='phone cannot be blank')
        parser.add_argument('relation', required=True, help='relation cannot be blank')
        args = parser.parse_args()

        try:
            new_contact = EmergencyContact(
                user_id=args['user_id'],
                name=args['name'],
                phone=args['phone'],
                relation=args['relation']
            )
            db.session.add(new_contact)
            db.session.commit()
            return {'message': 'Emergency contact created successfully'}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating emergency contact: %s', str(e))
            return {'message': 'Failed to create contact. Please try again.'}, 500

class EmergencyContactResource(Resource):
    @jwt_required()
    def get(self, contact_id):
        try:
            contact = EmergencyContact.query.get_or_404(contact_id)
            result = {'id': contact.id, 'user_id': contact.user_id, 'name': contact.name, 'phone': contact.phone, 'relation': contact.relation}
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching emergency contact: %s', str(e))
            return {'message': 'Error fetching contact. Please try again.'}, 500

    @jwt_required()
    def put(self, contact_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        parser.add_argument('phone', type=str)
        parser.add_argument('relation', type=str)
        args = parser.parse_args()

        try:
            contact = EmergencyContact.query.get_or_404(contact_id)
            if 'name' in args:
                contact.name = args['name']
            if 'phone' in args:
                contact.phone = args['phone']
            if 'relation' in args:
                contact.relation = args['relation']
            db.session.commit()
            return {'message': 'Emergency contact updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating emergency contact: %s', str(e))
            return {'message': 'Failed to update contact. Please try again.'}, 500

    @jwt_required()
    def delete(self, contact_id):
        try:
            contact = EmergencyContact.query.get_or_404(contact_id)
            db.session.delete(contact)
            db.session.commit()
            return {'message': 'Emergency contact deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting emergency contact: %s', str(e))
            return {'message': 'Failed to delete contact. Please try again.'}, 500
