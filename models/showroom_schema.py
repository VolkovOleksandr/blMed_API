from marshmallow import Schema, fields


# Schema for Showroom
class ShowroomSchema(Schema):
    id = fields.Integer(required=True)
    email = fields.String(required=True)
    address = fields.String(required=True)
    phone = fields.String(required=True)
