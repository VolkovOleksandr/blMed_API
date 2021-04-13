from flask_restful import Resource, reqparse, abort
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from sqlalchemy.exc import IntegrityError

from models.category import CategoryModel
from models.category_schema import CategorySchema
from models.db import db


# POST request fields
categoryPostArgs = reqparse.RequestParser()
categoryPostArgs.add_argument(
    "category", type=str, help="Category is required", required=True)


# Category controller
class CategoryController(MethodResource, Resource):
    # Get all category
    @doc(description='Get all category of products', tags=['Product'])
    @marshal_with(CategorySchema(many=True))
    def get(self):
        # Parse data from DB to JSON
        categorySchema = CategorySchema(many=True)
        categoryModel = CategoryModel.query.all()
        categoryJsonObj = categorySchema.dump(categoryModel)

        return categoryJsonObj

    # Create category
    @doc(description='Create new category. Argument ("category") - required', tags=['Product'])
    def post(self):
        # Get arguments from form
        args = categoryPostArgs.parse_args()

        # Create contact object
        schema = CategorySchema()
        category = CategoryModel()
        category.category = args["category"]

        # Save contact object
        try:
            db.session.add(category)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message="Category dublicated")

        return {"message": "Category successfully created", "category": schema.dump(category)}, 201
