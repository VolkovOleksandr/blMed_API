from flask_restful import Resource, abort, reqparse
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource

from models.service import ServiceModel
from models.service_schema import ServiceSchema
from models.db import db


# Controller for Service Switch


# POST request fields
servicesPatchArgs = reqparse.RequestParser()
servicesPatchArgs.add_argument(
    "title", type=str, help="Title is required", required=True)
servicesPatchArgs.add_argument("description", type=str,
                               help="Description is required", required=True)
servicesPatchArgs.add_argument("position", type=int,
                               help="Position is required", required=True)


# Services-controller for swich position
class ServiceSwitchController(MethodResource, Resource):
    # Get availeble all position
    @doc(description='Get all available position for specific ID', tags=['Services'])
    def get(self, service_id):
        arrayOfPosition = []
        schema = ServiceSchema(many=True)
        serviceObjects = ServiceModel.query.all()
        jsonServices = schema.dump(serviceObjects)

        # Adding all position to array but curent position object
        for service in jsonServices:
            if service_id != service['position']:
                arrayOfPosition.append(service['position'])
        # Check for minimum objects for swiching
        if len(arrayOfPosition) < 1:
            abort(404, message="At list must have two services")

        return {'positions': arrayOfPosition}

    # Update position

    @ doc(description='Update service position by ID. Takes one argument ("position") for swapping', tags=['Services'])
    def patch(self, service_id):
        # Check if ID exist
        if ServiceModel.query.get(service_id) == None:
            abort(404, message="Servise not found")

        schema = ServiceSchema()
        args = servicesPatchArgs.parse_args()
        # FromObj. Object which is gonna be swapped
        fromObject = ServiceModel.query.get(int(service_id))
        fromJsonObject = schema.dump(fromObject)
        fromPosition = fromJsonObject['position']

        # ToObj. An object which ON gonna be swapped
        toObject = ServiceModel.query.filter(
            ServiceModel.position == args['position']).first()
        toJsonObjParsed = schema.dump(toObject)

        # Check if Object with setted position exist
        if not toJsonObjParsed:
            abort(400, message="Servise position not find")
        toPosition = toJsonObjParsed['position']

        # Swapping Object positions
        fromObject.position = int(toPosition)
        toObject.position = int(fromPosition)

        # Save changes to DB
        db.session.commit()
        return {"message": "Service position successfully updated"}, 200
