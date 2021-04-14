from flask_restful import Resource, abort
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from sqlalchemy import desc

from models.product import Products
from models.product_schema import ProductSchema


# Products controller
class ProductsByLatestController(MethodResource, Resource):
    # Get latest products
    @doc(description='Get latest (max 10) products', tags=['Product'])
    @marshal_with(ProductSchema(many=True))
    def get(self):
        # Parse data from DB to JSON
        productSchema = ProductSchema(many=True)
        productsByLatest = Products.query.order_by(
            desc(Products.date_time)).limit(10).all()

        # Check if product exist
        if not productsByLatest:
            abort(404, message="NO latest products yet")

        latestProdJsonObj = productSchema.dump(productsByLatest)

        return latestProdJsonObj
