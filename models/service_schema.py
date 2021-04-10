from marshmallow import Schema, fields


# Schema for Services
class ServiceSchema(Schema):
    id = fields.Integer(required=True)
    title = fields.Str(required=True)
    description = fields.String(required=True)
    position = fields.Int(required=True)
