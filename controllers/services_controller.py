from flask_restful import Resource, reqparse
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource

from models.service import ServiceModel
from models.service_schema import ServiceSchema
from models.db import db


# POST request fields
servicesPostArgs = reqparse.RequestParser()
servicesPostArgs.add_argument(
    "title", type=str, help="Title is required", required=True)
servicesPostArgs.add_argument("description", type=str,
                              help="Description is required", required=True)


# Services controller
class ServicesController(MethodResource, Resource):
    # Get all services
    @doc(description='Get all services', tags=['Services'])
    @marshal_with(ServiceSchema(many=True))
    def get(self):
        result = ServiceModel.query.all()
        return result

    # Create new service
    @doc(description='Create new service. Takes two arguments ("title", "description") - required', tags=['Services'])
    def post(self):
        schema = ServiceSchema()
        args = servicesPostArgs.parse_args()
        newServise = ServiceModel()
        newServise.title = args["title"]
        newServise.description = args["description"]
        newServise.position = len(ServiceModel.query.all()) + 1

        db.session.add(newServise)
        db.session.commit()
        return {"message": "Service successfully created", "service": schema.dump(newServise)}, 201
