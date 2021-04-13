from marshmallow import Schema, fields


# Schema for Contacts
class CategorySchema(Schema):
    id = fields.Integer(required=True)
    category = fields.String(required=True)
