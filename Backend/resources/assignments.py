from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required
from models import db, Assignment, Driver, Place
from utils import log_user_activity

# Namespace
api = Namespace('assignments', description='Operations related to assignments')

# DTO Definitions
assignment_dto = api.model('Assignment', {
    'id': fields.Integer(description='Unique ID of the assignment'),
    'driver_id': fields.Integer(required=True, description='Driver ID for the assignment'),
    'place_id': fields.Integer(required=True, description='Place ID for the assignment'),
    'assigned_at': fields.String(required=True, description='Timestamp of the assignment')
})

create_assignment_dto = api.model('CreateAssignment', {
    'driver_id': fields.Integer(required=True, description='Driver ID for the assignment'),
    'place_id': fields.Integer(required=True, description='Place ID for the assignment'),
    'assigned_at': fields.String(required=True, description='Timestamp of the assignment (YYYY-MM-DD HH:MM:SS)')
})

update_assignment_dto = api.model('UpdateAssignment', {
    'driver_id': fields.Integer(description='Driver ID for the assignment'),
    'place_id': fields.Integer(description='Place ID for the assignment'),
    'assigned_at': fields.String(description='Timestamp of the assignment (YYYY-MM-DD HH:MM:SS)')
})


class AssignmentsResource(Resource):
    @log_user_activity('view_assignments')
    @jwt_required()
    @api.marshal_list_with(assignment_dto, envelope='data')
    def get(self):
        """Fetch all assignments"""
        try:
            assignments = Assignment.query.all()
            return assignments, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching assignments: %s', str(e))
            return {'message': 'Error fetching assignments. Please try again later.'}, 500

    @log_user_activity('create_assignment')
    @jwt_required()
    @api.expect(create_assignment_dto, validate=True)
    def post(self):
        """Create a new assignment"""
        data = api.payload

        driver = Driver.query.get(data['driver_id'])
        if not driver:
            return {'message': 'Driver not found'}, 404

        place = Place.query.get(data['place_id'])
        if not place:
            return {'message': 'Place not found'}, 404

        existing_assignment = Assignment.query.filter_by(
            driver_id=data['driver_id'],
            place_id=data['place_id'],
            assigned_at=data['assigned_at']
        ).first()
        if existing_assignment:
            return {'message': 'Driver is already assigned to this place at this time.'}, 400

        try:
            new_assignment = Assignment(
                driver_id=data['driver_id'],
                place_id=data['place_id'],
                assigned_at=data['assigned_at']
            )
            db.session.add(new_assignment)
            db.session.commit()
            return {'message': 'Assignment created successfully', 'data': {'id': new_assignment.id}}, 201
        except IntegrityError as e:
            app.logger.error('Integrity error while creating assignment: %s', str(e))
            db.session.rollback()
            return {'message': 'Failed to create assignment. Please check input data.'}, 400
        except SQLAlchemyError as e:
            app.logger.error('Error creating assignment: %s', str(e))
            return {'message': 'Failed to create assignment. Please try again later.'}, 500


class AssignmentResource(Resource):
    @jwt_required()
    @api.marshal_with(assignment_dto, envelope='data')
    def get(self, assignment_id):
        """Fetch a specific assignment"""
        try:
            assignment = Assignment.query.get_or_404(assignment_id)
            return assignment, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching assignment: %s', str(e))
            return {'message': 'Failed to fetch assignment. Please try again later.'}, 500

    @jwt_required()
    @api.expect(update_assignment_dto, validate=True)
    def put(self, assignment_id):
        """Update a specific assignment"""
        data = api.payload

        if 'driver_id' in data:
            driver = Driver.query.get(data['driver_id'])
            if not driver:
                return {'message': 'Driver not found'}, 404
        if 'place_id' in data:
            place = Place.query.get(data['place_id'])
            if not place:
                return {'message': 'Place not found'}, 404

        try:
            assignment = Assignment.query.get_or_404(assignment_id)

            if 'driver_id' in data:
                assignment.driver_id = data['driver_id']
            if 'place_id' in data:
                assignment.place_id = data['place_id']
            if 'assigned_at' in data:
                assignment.assigned_at = data['assigned_at']

            db.session.commit()
            return {'message': 'Assignment updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating assignment: %s', str(e))
            return {'message': 'Failed to update assignment. Please try again later.'}, 500

    @jwt_required()
    def delete(self, assignment_id):
        """Delete a specific assignment"""
        try:
            assignment = Assignment.query.get_or_404(assignment_id)
            db.session.delete(assignment)
            db.session.commit()
            return {'message': 'Assignment deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting assignment: %s', str(e))
            return {'message': 'Failed to delete assignment. Please try again later.'}, 500
