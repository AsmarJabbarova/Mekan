from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, RouteSegment
from utils import log_user_activity

# Namespace
api = Namespace('route_segments', description='Operations related to route segments')

# DTO Definitions
route_segment_model = api.model('RouteSegment', {
    'id': fields.Integer(description='The unique identifier of the route segment', readonly=True),
    'start_place_id': fields.Integer(required=True, description='The ID of the starting place'),
    'end_place_id': fields.Integer(required=True, description='The ID of the ending place'),
    'distance': fields.Float(required=True, description='The distance of the segment in kilometers'),
    'duration': fields.String(required=True, description='The estimated duration of the segment'),
})

create_route_segment_model = api.model('CreateRouteSegment', {
    'start_place_id': fields.Integer(required=True, description='The ID of the starting place'),
    'end_place_id': fields.Integer(required=True, description='The ID of the ending place'),
    'distance': fields.Float(required=True, description='The distance of the segment in kilometers'),
    'duration': fields.String(required=True, description='The estimated duration of the segment'),
})


class RouteSegmentsResource(Resource):
    @log_user_activity('view_route_segments')
    @jwt_required()
    @api.marshal_with(route_segment_model, as_list=True)
    def get(self):
        """Get all route segments."""
        try:
            segments = RouteSegment.query.all()
            return segments, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching route segments: %s', str(e))
            api.abort(500, 'Error fetching route segments. Please try again.')

    @log_user_activity('create_route_segment')
    @jwt_required()
    @api.expect(create_route_segment_model, validate=True)
    @api.marshal_with(route_segment_model, code=201)
    def post(self):
        """Create a new route segment."""
        data = api.payload
        try:
            new_segment = RouteSegment(
                start_place_id=data['start_place_id'],
                end_place_id=data['end_place_id'],
                distance=data['distance'],
                duration=data['duration']
            )
            db.session.add(new_segment)
            db.session.commit()
            return new_segment, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating route segment: %s', str(e))
            api.abort(500, 'Failed to create route segment. Please try again.')


class RouteSegmentResource(Resource):
    @jwt_required()
    @api.marshal_with(route_segment_model)
    def get(self, segment_id):
        """Get a specific route segment by its ID."""
        try:
            segment = RouteSegment.query.get_or_404(segment_id)
            return segment, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching route segment with ID %s: %s', segment_id, str(e))
            api.abort(500, 'Error fetching route segment. Please try again.')

    @jwt_required()
    @api.expect(create_route_segment_model, validate=True)
    @api.marshal_with(route_segment_model)
    def put(self, segment_id):
        """Update a route segment."""
        data = api.payload
        try:
            segment = RouteSegment.query.get_or_404(segment_id)
            segment.start_place_id = data.get('start_place_id', segment.start_place_id)
            segment.end_place_id = data.get('end_place_id', segment.end_place_id)
            segment.distance = data.get('distance', segment.distance)
            segment.duration = data.get('duration', segment.duration)
            db.session.commit()
            return segment, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating route segment with ID %s: %s', segment_id, str(e))
            api.abort(500, 'Failed to update route segment. Please try again.')

    @jwt_required()
    def delete(self, segment_id):
        """Delete a route segment."""
        try:
            segment = RouteSegment.query.get_or_404(segment_id)
            db.session.delete(segment)
            db.session.commit()
            return {'message': 'Route segment deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting route segment with ID %s: %s', segment_id, str(e))
            api.abort(500, 'Failed to delete route segment. Please try again.')
