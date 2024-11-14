from flask import current_app as app, jsonify
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, Assignment, Driver, Place
from utils import log_user_activity

class AssignmentsResource(Resource):
    @log_user_activity('view_assignments')
    @jwt_required()
    def get(self):
        try:
            assignments = Assignment.query.all()
            result = [{'id': assignment.id, 'driver_id': assignment.driver_id, 'place_id': assignment.place_id, 'assigned_at': assignment.assigned_at} for assignment in assignments]
            return jsonify({'data': result}), 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching assignments: %s', str(e))
            return {'message': 'Error fetching assignments. Please try again later.'}, 500

    @log_user_activity('create_assignment')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('driver_id', required=True, help='driver_id cannot be blank')
        parser.add_argument('place_id', required=True, help='place_id cannot be blank')
        parser.add_argument('assigned_at', required=True, help='assigned_at cannot be blank')
        args = parser.parse_args()

        driver = Driver.query.get(args['driver_id'])
        if not driver:
            return {'message': 'Driver not found'}, 404

        place = Place.query.get(args['place_id'])
        if not place:
            return {'message': 'Place not found'}, 404

        existing_assignment = Assignment.query.filter_by(driver_id=args['driver_id'], place_id=args['place_id'], assigned_at=args['assigned_at']).first()
        if existing_assignment:
            return {'message': 'Driver is already assigned to this place at this time.'}, 400

        try:
            new_assignment = Assignment(
                driver_id=args['driver_id'],
                place_id=args['place_id'],
                assigned_at=args['assigned_at']
            )
            db.session.add(new_assignment)
            db.session.commit()
            return {'message': 'Assignment created successfully', 'data': {'id': new_assignment.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating assignment: %s', str(e))
            return {'message': 'Failed to create assignment. Please try again later.'}, 500

class AssignmentResource(Resource):
    @jwt_required()
    def get(self, assignment_id):
        try:
            assignment = Assignment.query.get_or_404(assignment_id)
            result = {
                'id': assignment.id,
                'driver_id': assignment.driver_id,
                'place_id': assignment.place_id,
                'assigned_at': assignment.assigned_at
            }
            return jsonify({'data': result}), 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching assignment: %s', str(e))
            return {'message': 'Failed to fetch assignment. Please try again later.'}, 500

    @jwt_required()
    def put(self, assignment_id):
        parser = reqparse.RequestParser()
        parser.add_argument('driver_id', type=int)
        parser.add_argument('place_id', type=int)
        parser.add_argument('assigned_at', type=str)
        args = parser.parse_args()

        if 'driver_id' in args:
            driver = Driver.query.get(args['driver_id'])
            if not driver:
                return {'message': 'Driver not found'}, 404
        if 'place_id' in args:
            place = Place.query.get(args['place_id'])
            if not place:
                return {'message': 'Place not found'}, 404

        try:
            assignment = Assignment.query.get_or_404(assignment_id)

            if 'driver_id' in args:
                assignment.driver_id = args['driver_id']
            if 'place_id' in args:
                assignment.place_id = args['place_id']
            if 'assigned_at' in args:
                assignment.assigned_at = args['assigned_at']

            db.session.commit()
            return {'message': 'Assignment updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating assignment: %s', str(e))
            return {'message': 'Failed to update assignment. Please try again later.'}, 500

    @jwt_required()
    def delete(self, assignment_id):
        try:
            assignment = Assignment.query.get_or_404(assignment_id)
            db.session.delete(assignment)
            db.session.commit()
            return {'message': 'Assignment deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting assignment: %s', str(e))
            return {'message': 'Failed to delete assignment. Please try again later.'}, 500
