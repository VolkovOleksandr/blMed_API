from marshmallow import Schema, fields


# Schema for Product
class ProductSchema(Schema):
    id = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
    image_url = fields.String()
    name = fields.String(required=True)
    description = fields.String(required=True)
    brand = fields.String()
    date_time = fields.String()
    featured = fields.Boolean()
