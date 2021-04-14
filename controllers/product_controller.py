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
    "category_id", type=int, help="Category id is required", required=True)
ProductPutArgs.add_argument("image_url", type=str)
ProductPutArgs.add_argument(
    "name", type=str, help="Name is required", required=True)
ProductPutArgs.add_argument(
    "description", type=str, help="Description is required", required=True)
ProductPutArgs.add_argument(
    "brand", type=str)
ProductPutArgs.add_argument("featured", type=bool)


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

    # Edit product by ID
    @doc(description='Edit product by ID. Argument ("category_id", "image_url", "name", "description", "brand", "featured")', tags=['Product'])
    def put(self, product_id):
        # Get arguments from form
        args = ProductPutArgs.parse_args()

        # Get product form DB
        schema = ProductSchema()
        product = Products.query.get(product_id)

        if not product:
            abort(404, message="Product not found")

        product.category_id = args["category_id"]
        product.image_url = args["image_url"]
        product.name = args["name"]
        product.description = args["description"]
        product.brand = args["brand"]
        product.featured = args["featured"]

        # Save product object
        try:
            db.session.commit()
        except IntegrityError as e:
            abort(400, message="Product dublicated")

        return {"message": "Product successfully updated", "product": schema.dump(product)}, 201
