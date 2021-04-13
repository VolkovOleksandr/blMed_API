from flask_restful import Resource, reqparse, abort
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from sqlalchemy.exc import IntegrityError

from models.categories import Categories
from models.category_schema import CategorySchema
from models.db import db


# POST request fields
categoryPutArgs = reqparse.RequestParser()
categoryPutArgs.add_argument(
    "category", type=str, help="Category is required", required=True)


# Category controller
class CategoryController(MethodResource, Resource):
    # Get category by ID
    @doc(description='Get category by ID of product', tags=['Product'])
    @marshal_with(CategorySchema())
    def get(self, category_id):
        # Parse data from DB to JSON
        categorySchema = CategorySchema()
        categoryModel = Categories.query.get(category_id)
        # Check if category exist
        if not categoryModel:
            abort(404, message="Category not found")

        categoryJsonObj = categorySchema.dump(categoryModel)

        return categoryJsonObj

    # Edit category by ID
    @doc(description='Edit category. Argument ("category") - required', tags=['Product'])
    def put(self, category_id):
        # Get arguments from form
        args = categoryPutArgs.parse_args()

        # Create contact object
        schema = CategorySchema()
        category = Categories.query.get(category_id)

        if not category:
            abort(404, message="Category not found")

        category.category = args["category"]

        # Save contact object
        try:
            db.session.commit()
        except IntegrityError as e:
            abort(400, message="Category dublicated")

        return {"message": "Category successfully created", "category": schema.dump(category)}, 201

    # DELETE category by ID
    @doc(description='Delete category by ID of product', tags=['Product'])
    def delete(self, category_id):
        # Parse data from DB to JSON
        categoryObject = Categories.query.get(category_id)

        # Check if category exist
        if not categoryObject:
            abort(404, message="Category not found")

        db.session.delete(categoryObject)
        db.session.commit()
        return "Service successfully deleted", 204
