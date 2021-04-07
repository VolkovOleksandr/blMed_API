from flask_restful import Resource, abort
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from models.service import ServiceModel

from models.service_schema import ServiceSchema


# Controller for Service
# Get services by id
class ServiceController(MethodResource, Resource):
    @doc(description='Get service by id', tags=['Services'])
    @marshal_with(ServiceSchema)
    def get(self, service_id):
        if ServiceModel.query.get(service_id) == None:
            abort(404, message="Servise not found")
        result = ServiceModel.query.get(int(service_id))
        return result
