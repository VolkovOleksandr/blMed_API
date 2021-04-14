from flask_restful import Resource, abort
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource

from models.product import Products
from models.product_schema import ProductSchema


# Products controller
class ProductsByCategoryController(MethodResource, Resource):
    # Get All products
    @doc(description='Get products by category ID', tags=['Product'])
    @marshal_with(ProductSchema(many=True))
    def get(self, category_id):
        # Parse data from DB to JSON
        productSchema = ProductSchema(many=True)
        productsByCategory = Products.query.filter_by(
            category_id=category_id).all()

        # Check if product exist in category
        if not productsByCategory:
            abort(404, message="NO products yet in this category")

        categoryJsonObj = productSchema.dump(productsByCategory)

        return categoryJsonObj
