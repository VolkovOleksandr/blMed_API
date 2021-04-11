from marshmallow import Schema, fields


# Schema for Contacts
class ContactSchema(Schema):
    id = fields.Integer(required=True)
    person = fields.String(required=True)
    email = fields.String(required=True)
    fax = fields.String()
    phone = fields.String(required=True)
