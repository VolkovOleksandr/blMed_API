from flask_restful import Resource, fields, marshal_with
from models.service import ServiceModel

# Controller for Services

# JSONE decorator
service_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'position': fields.Integer
}


# Get all services

class ServicesController(Resource):
    @marshal_with(service_fields)
    def get(self):
        result = ServiceModel.query.all()
        return result
