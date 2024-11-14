from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, RouteSegment
from utils import log_user_activity

class RouteSegmentsResource(Resource):
    @log_user_activity('view_route_segments')
    @jwt_required()
    def get(self):
        try:
            segments = RouteSegment.query.all()
            result = [{'id': segment.id, 'start_place_id': segment.start_place_id, 'end_place_id': segment.end_place_id, 'distance': segment.distance, 'duration': segment.duration} for segment in segments]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching route segments: %s', str(e))
            return {'message': 'Error fetching segments. Please try again.'}, 500

    @log_user_activity('create_route_segment')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('start_place_id', required=True, help='start_place_id cannot be blank')
        parser.add_argument('end_place_id', required=True, help='end_place_id cannot be blank')
        parser.add_argument('distance', required=True, type=float, help='distance cannot be blank')
        parser.add_argument('duration', required=True, help='duration cannot be blank')
        args = parser.parse_args()

        try:
            new_segment = RouteSegment(
                start_place_id=args['start_place_id'],
                end_place_id=args['end_place_id'],
                distance=args['distance'],
                duration=args['duration']
            )
            db.session.add(new_segment)
            db.session.commit()
            return {'message': 'Route segment created successfully', 'data': {'id': new_segment.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating route segment: %s', str(e))
            return {'message': 'Failed to create route segment. Please try again.'}, 500

class RouteSegmentResource(Resource):
    @jwt_required()
    def get(self, segment_id):
        try:
            segment = RouteSegment.query.get_or_404(segment_id)
            result = {
                'id': segment.id,
                'start_place_id': segment.start_place_id,
                'end_place_id': segment.end_place_id,
                'distance': segment.distance,
                'duration': segment.duration
            }
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching route segment: %s', str(e))
            return {'message': 'Error fetching segment. Please try again.'}, 500

    @jwt_required()
    def put(self, segment_id):
        parser = reqparse.RequestParser()
        parser.add_argument('start_place_id', type=int)
        parser.add_argument('end_place_id', type=int)
        parser.add_argument('distance', type=float)
        parser.add_argument('duration', type=str)
        args = parser.parse_args()

        try:
            segment = RouteSegment.query.get_or_404(segment_id)
            if 'start_place_id' in args:
                segment.start_place_id = args['start_place_id']
            if 'end_place_id' in args:
                segment.end_place_id = args['end_place_id']
            if 'distance' in args:
                segment.distance = args['distance']
            if 'duration' in args:
                segment.duration = args['duration']
            db.session.commit()
            return {'message': 'Route segment updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating route segment: %s', str(e))
            return {'message': 'Failed to update route segment. Please try again.'}, 500

    @jwt_required()
    def delete(self, segment_id):
        try:
            segment = RouteSegment.query.get_or_404(segment_id)
            db.session.delete(segment)
            db.session.commit()
            return {'message': 'Route segment deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting route segment: %s', str(e))
            return {'message': 'Failed to delete route segment. Please try again.'}, 500
