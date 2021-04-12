from models.contact import ContactModel
from flask_restful import Resource, reqparse, abort
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from sqlalchemy.exc import IntegrityError

from models.showroom import ShowroomModel
from models.showroom_schema import ShowroomSchema
from models.db import db


# POST request fields
contactPostArgs = reqparse.RequestParser()
contactPostArgs.add_argument(
    "address", type=str, help="Address is required", required=True)
contactPostArgs.add_argument(
    "email", type=str, help="Email is required", required=True)
contactPostArgs.add_argument(
    "phone", type=str, help="Phone is required", required=True)


# Showroom by ID controller
class ShowroomController(MethodResource, Resource):
    # Get showroom by ID
    @doc(description='Get showroom by ID', tags=['Contact'])
    @marshal_with(ShowroomSchema())
    def get(self, shoowroom_id):
        # Parse data from DB to JSON
        showroomSchema = ShowroomSchema()
        showroomModel = ShowroomModel.query.get(shoowroom_id)
        showroomJsonObj = showroomSchema.dump(showroomModel)

        # Check if Showroom exist
        if not showroomJsonObj:
            abort(400, message="Showroom not exist")

        # Prepeied result for all showrooms
        return showroomJsonObj

    # Edit showroom
    @doc(description='Edit showroom. Arguments ("address", "email", "phone") - required', tags=['Contact'])
    def put(self, shoowroom_id):
        # Get arguments from form and DB
        args = contactPostArgs.parse_args()
        showroom = ShowroomModel.query.get(shoowroom_id)
        schema = ShowroomSchema()

        # Edit showroom object
        showroom.address = args["address"]
        showroom.email = args["email"]
        showroom.phone = args["phone"]

        # Save showroom object
        try:
            db.session.commit()
        except IntegrityError as e:
            abort(400, message="Showroom dublicated")

        return {"message": "Showroom successfully created", "contact": schema.dump(showroom)}, 201

    # Delete showroom
    @doc(description='Delete showroom by id', tags=['Contact'])
    def delete(self, shoowroom_id):
        if ShowroomModel.query.get(shoowroom_id) == None:
            abort(404, message="Showroom not found")
        deleteShowroomById = ShowroomModel.query.get(int(shoowroom_id))
        db.session.delete(deleteShowroomById)
        db.session.commit()
        return "Showroom successfully deleted", 204
