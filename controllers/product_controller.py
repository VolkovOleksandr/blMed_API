from flask_restful import Resource, reqparse, abort
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from sqlalchemy.exc import IntegrityError

from models.product import Products
from models.product_schema import ProductSchema
from models.db import db


# PUT request fields
ProductPutArgs = reqparse.RequestParser()
ProductPutArgs.add_argument(
    "category", type=str, help="Category is required", required=True)


# Product controller
class ProductController(MethodResource, Resource):
    # Get product by ID
    @doc(description='Get product by ID', tags=['Product'])
    @marshal_with(ProductSchema())
    def get(self, product_id):
        # Parse data from DB to JSON
        productSchema = ProductSchema()
        productModel = Products.query.get(product_id)
        # Check if product exist
        if not productModel:
            abort(404, message="Product not found")

        productJsonObj = productSchema.dump(productModel)

        return productJsonObj

    # DELETE product by ID
    @doc(description='Delete product by ID', tags=['Product'])
    def delete(self, product_id):
        # Parse data from DB to JSON
        productObject = Products.query.get(product_id)

        # Check if product exist
        if not productObject:
            abort(404, message="Product not found")

        db.session.delete(productObject)
        db.session.commit()
        return "Product successfully deleted", 204

    # # Edit category by ID
    # @doc(description='Edit category. Argument ("category") - required', tags=['Category'])
    # def put(self, category_id):
    #     # Get arguments from form
    #     args = ProductPutArgs.parse_args()

    #     # Create contact object
    #     schema = CategorySchema()
    #     category = Categories.query.get(category_id)

    #     if not category:
    #         abort(404, message="Category not found")

    #     category.category = args["category"]

    #     # Save contact object
    #     try:
    #         db.session.commit()
    #     except IntegrityError as e:
    #         abort(400, message="Category dublicated")

    #     return {"message": "Category successfully created", "category": schema.dump(category)}, 201

    #
