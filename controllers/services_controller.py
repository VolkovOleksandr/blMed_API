from flask_restful import Resource
from flask_apispec import marshal_with, doc
from models.service import ServiceModel
from flask_apispec.views import MethodResource

from models.service_schema import ServiceSchema


# Services controller
# Get all services
class ServicesController(MethodResource, Resource):
    @doc(description='Get all services', tags=['Services'])
    @marshal_with(ServiceSchema(many=True))
    def get(self):
        result = ServiceModel.query.all()
        return result
