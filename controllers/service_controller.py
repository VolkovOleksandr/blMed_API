from flask_restful import Resource, fields, marshal_with
from models.service import ServiceModel

# Controller for Service

# JSONE decorator
service_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'position': fields.Integer
}


# Get services by id

class ServiceController(Resource):
    @marshal_with(service_fields)
    def get(self, service_id):
        result = ServiceModel.query.get(int(service_id))
        return result
