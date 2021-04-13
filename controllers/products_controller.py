from flask_restful import Resource, reqparse, abort
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from sqlalchemy.exc import IntegrityError

from models.product import Products
from models.product_schema import ProductSchema
from models.db import db


# POST request fields
productPostArgs = reqparse.RequestParser()
productPostArgs.add_argument(
    "category_id", type=int, help="Category ID is required", required=True)
productPostArgs.add_argument(
    "image_url", type=str)
productPostArgs.add_argument(
    "name", type=str, help="Name of productis required", required=True)
productPostArgs.add_argument(
    "description", type=str, help="Description is required", required=True)
productPostArgs.add_argument(
    "brand", type=str)
productPostArgs.add_argument(
    "featured", type=bool)


# Products controller
class ProductsController(MethodResource, Resource):
    # Get All products
    @doc(description='Get all products', tags=['Product'])
    @marshal_with(ProductSchema(many=True))
    def get(self):
        # Parse data from DB to JSON
        categorySchema = ProductSchema(many=True)
        categoryModel = Products.query.all()

        # Check if product exist
        if not categoryModel:
            abort(404, message="NO products yet")

        categoryJsonObj = categorySchema.dump(categoryModel)

        return categoryJsonObj

    # Create new product

    @doc(description='Create new product. Argument ("category_id", "name", "description") - required', tags=['Product'])
    def post(self):
        # Get arguments from form
        args = productPostArgs.parse_args()

        # Create contact object
        schema = ProductSchema()
        product = Products()
        product.category_id = args["category_id"]
        product.image_url = args["image_url"]
        product.name = args["name"]
        product.description = args["description"]
        product.brand = args["brand"]
        product.featured = args["featured"]

        # Store product to DB
        try:
            db.session.add(product)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message="Product dublicated")

        return {"message": "Product successfully created", "product": schema.dump(product)}, 201
