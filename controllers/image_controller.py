from flask_restful import Resource, reqparse, abort
from flask_apispec.views import MethodResource
from flask_apispec import doc
from werkzeug.datastructures import FileStorage
from PIL import Image
import datetime

# POST file field
categoryPutArgs = reqparse.RequestParser()
categoryPutArgs.add_argument(
    "image", type=FileStorage, location='files', action='append')


# Image controller
class ImageController(MethodResource, Resource):

    # Add new images to product
    @doc(description='Add new  images to product. Argument ("image"). Return images array', tags=['Product'])
    def post(self):
        # Get arguments from form
        args = categoryPutArgs.parse_args()
        images_file = args['image']

        # Check all images from args
        imageIdArray = []
        for image in images_file:
            # Check if mime type of images acceptable
            if image.content_type == 'image/png' or image.content_type == 'image/jpeg' or image.content_type == 'image/heic':
                # Prepearing name for image like unique ID
                dateTimeForId = str(datetime.datetime.now())
                imageId = dateTimeForId.replace(" ", "_")
                mine = getMime(image.content_type)
                imageName = imageId + mine
                # Resize and save image (max height or wigth 500px)
                newImage = Image.open(image)
                width, height = newImage.size
                if height >= width:
                    newImageResize = newImage.resize(
                        (int((500*width)/height), 500))
                else:
                    newImageResize = newImage.resize(
                        (500, int((500*height)/width)))
                newImageResize.save(
                    './images/{imageName}'.format(imageName=imageName))
                imageIdArray.append(imageName)
            else:
                abort(400, message="Image type should be .png .jpeg .heic")

        return {"imagesArray": imageIdArray}


def toPng():
    return '.png'


def toJpeg():
    return '.jpeg'


def toHeic():
    return '.heic'


switcher = {
    'image/png': toPng,
    'image/jpeg': toJpeg,
    'image/heic': toHeic
}


def getMime(argument):
    func = switcher.get(argument)
    return func()
