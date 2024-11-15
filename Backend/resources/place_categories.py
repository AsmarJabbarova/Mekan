from flask import current_app as app
from flask_restx import Resource, Namespace, fields
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, PlaceCategory
from utils import log_user_activity

# Namespace
api = Namespace('place_categories', description='Operations related to place categories')

# DTO Definitions
place_category_dto = api.model('PlaceCategory', {
    'id': fields.Integer(description='Unique ID of the category'),
    'name': fields.String(required=True, description='Name of the category')
})

create_place_category_dto = api.model('CreatePlaceCategory', {
    'name': fields.String(required=True, description='Name of the category')
})


class PlaceCategoriesResource(Resource):
    @log_user_activity('view_place_categories')
    @jwt_required()
    @api.marshal_list_with(place_category_dto, envelope='data')
    def get(self):
        """Fetch all place categories"""
        try:
            categories = PlaceCategory.query.all()
            return categories, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching place categories: %s', str(e))
            return {'message': 'Error fetching categories. Please try again.'}, 500

    @log_user_activity('create_place_category')
    @jwt_required()
    @api.expect(create_place_category_dto, validate=True)
    def post(self):
        """Create a new place category"""
        data = api.payload

        if PlaceCategory.query.filter_by(name=data['name']).first():
            return {'message': 'Category already exists'}, 400

        try:
            new_category = PlaceCategory(name=data['name'])
            db.session.add(new_category)
            db.session.commit()
            return {'message': 'Category created successfully', 'data': {'id': new_category.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating category: %s', str(e))
            return {'message': 'Failed to create category. Please try again.'}, 500


class PlaceCategoryResource(Resource):
    @jwt_required()
    @api.marshal_with(place_category_dto, envelope='data')
    def get(self, category_id):
        """Fetch a specific place category"""
        try:
            category = PlaceCategory.query.get_or_404(category_id)
            return category, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching category: %s', str(e))
            return {'message': 'Error fetching category. Please try again.'}, 500

    @jwt_required()
    @api.expect(create_place_category_dto, validate=True)
    def put(self, category_id):
        """Update a specific place category"""
        data = api.payload

        try:
            category = PlaceCategory.query.get_or_404(category_id)

            if 'name' in data:
                category.name = data['name']

            db.session.commit()
            return {'message': 'Category updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating category: %s', str(e))
            return {'message': 'Failed to update category. Please try again.'}, 500

    @jwt_required()
    def delete(self, category_id):
        """Delete a specific place category"""
        try:
            category = PlaceCategory.query.get_or_404(category_id)
            db.session.delete(category)
            db.session.commit()
            return {'message': 'Category deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting category: %s', str(e))
            return {'message': 'Failed to delete category. Please try again.'}, 500
