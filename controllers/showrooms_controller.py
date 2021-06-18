from flask import jsonify
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
    "address", type=str, help="Adress is required", required=True)
contactPostArgs.add_argument("email", type=str,
                             help="Email is required", required=True)
contactPostArgs.add_argument("phone", type=str,
                             help="Phone is required", required=True)


# Showroom controller
class ShowroomsController(MethodResource, Resource):
    # Get all showrooms
    @doc(description='Get all showrooms', tags=['Contact'])
    @marshal_with(ShowroomSchema(many=True))
    def get(self):
        # Parse data from DB to JSON
        showroomSchema = ShowroomSchema(many=True)
        showroomModel = ShowroomModel.query.all()
        showroomJsonObj = showroomSchema.dump(showroomModel)

        # Check if Showroom exist
        if not showroomJsonObj:
            abort(400, message="Showrooms not exist")

        # Prepeied result for all showrooms
        showroomsArray = []
        for showroom in showroomJsonObj:
            showroomInfo = {}
            phoneArr, emailArr = [], []
            showroomInfo['id'] = showroom['id']
            showroomInfo['address'] = showroom['address']

            for email in showroom['email'].split(';'):
                emailArr.append(email.rstrip().lstrip())
            showroomInfo['email'] = emailArr

            for phone in showroom['phone'].split(';'):
                phoneArr.append(phone.rstrip().lstrip())
            showroomInfo['phone'] = phoneArr

            showroomsArray.append(showroomInfo)
        return jsonify(showroomsArray)

    # Create showroom
    @doc(description='Add new showroom. Arguments ("address", "email", "phone") - required', tags=['Contact'])
    def post(self):
        # Get arguments from form
        args = contactPostArgs.parse_args()

        # Create showroom object
        schema = ShowroomSchema()
        showroomInfo = ShowroomModel()
        showroomInfo.address = args["address"]
        showroomInfo.email = args["email"]
        showroomInfo.phone = args["phone"]

        # Save showroom object
        try:
            db.session.add(showroomInfo)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message="Showroom dublicated")

        return {"message": "Showroom successfully created", "contact": schema.dump(showroomInfo)}, 201
