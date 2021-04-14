from flask_restful import Resource, abort
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource

from models.product import Products
from models.product_schema import ProductSchema


# Products controller
class ProductsByFeaturedController(MethodResource, Resource):
    # Get All products
    @doc(description='Get featured products', tags=['Product'])
    @marshal_with(ProductSchema(many=True))
    def get(self):
        # Parse data from DB to JSON
        productSchema = ProductSchema(many=True)
        productsByFeatured = Products.query.filter_by(
            featured=True).all()

        # Check if product exist
        if not productsByFeatured:
            abort(404, message="NO featured products")

        categoryJsonObj = productSchema.dump(productsByFeatured)

        return categoryJsonObj
