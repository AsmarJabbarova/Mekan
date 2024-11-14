from flask import current_app as app
from flask_restx import Resource, reqparse
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import jwt_required
from models import db, PlaceCategory
from utils import log_user_activity

class PlaceCategoriesResource(Resource):
    @log_user_activity('view_place_categories')
    @jwt_required()
    def get(self):
        try:
            categories = PlaceCategory.query.all()
            result = [{'id': category.id, 'name': category.name} for category in categories]
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching place categories: %s', str(e))
            return {'message': 'Error fetching categories. Please try again.'}, 500

    @log_user_activity('create_place_category')
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help='Name cannot be blank')
        args = parser.parse_args()

        existing_category = PlaceCategory.query.filter_by(name=args['name']).first()
        if existing_category:
            return {'message': 'Category already exists'}, 400

        try:
            new_category = PlaceCategory(name=args['name'])
            db.session.add(new_category)
            db.session.commit()
            return {'message': 'Category created successfully', 'data': {'id': new_category.id}}, 201
        except SQLAlchemyError as e:
            app.logger.error('Error creating category: %s', str(e))
            return {'message': 'Failed to create category. Please try again.'}, 500

class PlaceCategoryResource(Resource):
    @jwt_required()
    def get(self, category_id):
        try:
            category = PlaceCategory.query.get_or_404(category_id)
            result = {'id': category.id, 'name': category.name}
            return {'data': result}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error fetching category: %s', str(e))
            return {'message': 'Error fetching category. Please try again.'}, 500

    @jwt_required()
    def put(self, category_id):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str)
        args = parser.parse_args()

        try:
            category = PlaceCategory.query.get_or_404(category_id)
            if 'name' in args:
                category.name = args['name']
            db.session.commit()
            return {'message': 'Category updated successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error updating category: %s', str(e))
            return {'message': 'Failed to update category. Please try again.'}, 500

    @jwt_required()
    def delete(self, category_id):
        try:
            category = PlaceCategory.query.get_or_404(category_id)
            db.session.delete(category)
            db.session.commit()
            return {'message': 'Category deleted successfully'}, 200
        except SQLAlchemyError as e:
            app.logger.error('Error deleting category: %s', str(e))
            return {'message': 'Failed to delete category. Please try again.'}, 500
