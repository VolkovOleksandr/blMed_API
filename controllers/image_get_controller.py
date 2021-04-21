from flask_restful import Resource, abort
from flask import send_from_directory
from flask_apispec.views import MethodResource
from flask_apispec import doc
import os

# Path to image folder
IMAGE_DIRECTORY = os.getcwd() + "/images/"


# Get Image by name controller
class ImageGetController(MethodResource, Resource):
    # Get image by name
    @doc(description='Get images by name', tags=['Product'])
    def get(self, image_name):
        if not os.path.exists(IMAGE_DIRECTORY + image_name):
            abort(404, message="Image not exist")

        return send_from_directory(IMAGE_DIRECTORY, image_name)
