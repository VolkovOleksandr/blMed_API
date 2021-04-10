from flask_restful import Resource, abort, reqparse
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from sqlalchemy.exc import IntegrityError

from models.service import ServiceModel
from models.service_schema import ServiceSchema
from models.db import db


# POST request fields
servicesPostArgs = reqparse.RequestParser()
servicesPostArgs.add_argument(
    "title", type=str, help="Title is required", required=True)
servicesPostArgs.add_argument("description", type=str,
                              help="Description is required", required=True)

# Controller for Service


class ServiceController(MethodResource, Resource):
    # Get services by id
    @doc(description='Get service by id', tags=['Services'])
    @marshal_with(ServiceSchema)
    def get(self, service_id):
        if ServiceModel.query.get(service_id) == None:
            abort(404, message="Servise not found")
        result = ServiceModel.query.get(int(service_id))
        return result

    # Delete service
    @doc(description='Delete service by id', tags=['Services'])
    def delete(self, service_id):
        if ServiceModel.query.get(service_id) == None:
            abort(404, message="Servise not found")
        deleteServiceId = ServiceModel.query.get(int(service_id))
        db.session.delete(deleteServiceId)
        db.session.commit()
        return "Service successfully deleted", 204

    # Update services by id
    @doc(description='Update service by id. Takes two arguments ("title", "description")', tags=['Services'])
    @marshal_with(ServiceSchema)
    def put(self, service_id):
        args = servicesPostArgs.parse_args()

        # Check if service exist
        if ServiceModel.query.get(service_id) == None:
            abort(404, message="Servise not found")

        # Get service by id from DB
        serviceUpdObject = ServiceModel.query.get(int(service_id))
        serviceUpdObject.title = args['title']
        serviceUpdObject.description = args['description']

        # Save changes to DB
        try:
            db.session.commit()
        except IntegrityError as e:
            abort(400, message="Service dublicated")
        return serviceUpdObject
