from flask import jsonify
from flask_restful import Resource, reqparse, abort
from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from sqlalchemy.exc import IntegrityError

from models.contact import ContactModel
from models.contact_schema import ContactSchema
from models.db import db


# POST request fields
contactPostArgs = reqparse.RequestParser()
contactPostArgs.add_argument(
    "person", type=str, help="Person is required", required=True)
contactPostArgs.add_argument("email", type=str,
                             help="Email is required", required=True)
contactPostArgs.add_argument("phone", type=str,
                             help="Phone is required", required=True)
contactPostArgs.add_argument("fax", type=str)


# Contact controller
class ContactController(MethodResource, Resource):
    # Get contact info
    @doc(description='Get contact info', tags=['Contact'])
    @marshal_with(ContactSchema())
    def get(self):
        # Parse data from DB to JSON
        contactSchema = ContactSchema()
        contactModel = ContactModel.query.first()
        contactJsonObj = contactSchema.dump(contactModel)
        if contactModel == None:
            return abort(404, message="Contact info not found")
        # Prepeied result contact info
        contactInfo = {}
        phoneArr, faxArr, emailArr = [], [], []
        contactInfo['person'] = contactJsonObj['person']

        for email in contactJsonObj['email'].split(';'):
            emailArr.append(email.rstrip().lstrip())
        contactInfo['email'] = emailArr

        # Check if Fax exist if not return empty array
        if contactJsonObj['fax'] == None:
            contactInfo['fax'] = faxArr
        else:
            for fax in contactJsonObj['fax'].split(';'):
                faxArr.append(fax.rstrip().lstrip())
            contactInfo['fax'] = faxArr

        for phone in contactJsonObj['phone'].split(';'):
            phoneArr.append(phone.rstrip().lstrip())
        contactInfo['phone'] = phoneArr

        return jsonify(contactInfo)

    # Create contact
    @doc(description='Create contact info. Arguments ("person", "email", "phone") - required, "fax" not required', tags=['Contact'])
    def post(self):
        # Check if info already in DB
        checkInfo = ContactModel.query.first()
        if checkInfo:
            abort(400, message="Contact info already created. Try to edit")

        # Get arguments from form
        args = contactPostArgs.parse_args()

        # Create contact object
        schema = ContactSchema()
        contactInfo = ContactModel()
        contactInfo.person = args["person"]
        contactInfo.email = args["email"]
        contactInfo.phone = args["phone"]
        if args["fax"] != "":
            contactInfo.fax = args["fax"]

        # Save contact object
        try:
            db.session.add(contactInfo)
            db.session.commit()
        except IntegrityError as e:
            abort(400, message="Contact dublicated")

        return {"message": "Contact successfully created", "contact": schema.dump(contactInfo)}, 201
