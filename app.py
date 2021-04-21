from flask import Flask
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_cors import CORS
import os

from models.db import db

# Service Controllers
from controllers.services_controller import ServicesController
from controllers.service_controller import ServiceController
from controllers.service_swich_controller import ServiceSwitchController
# Contact controllers
from controllers.contact_controller import ContactController
from controllers.showrooms_controller import ShowroomsController
from controllers.showroom_controller import ShowroomController
# Category controllers
from controllers.categories_controller import CategoriesController
from controllers.category_controller import CategoryController
# Product controllers
from controllers.products_controller import ProductsController
from controllers.products_by_category_controller import ProductsByCategoryController
from controllers.product_by_featured import ProductsByFeaturedController
from controllers.product_latest_controller import ProductsByLatestController
from controllers.product_controller import ProductController
from controllers.image_controller import ImageController
from controllers.image_get_controller import ImageGetController

# init app
UPLOAD_IMAGE_DIRECTORY = os.getcwd() + "/images/"

if not os.path.exists(UPLOAD_IMAGE_DIRECTORY):
    os.makedirs(UPLOAD_IMAGE_DIRECTORY)


def initApp():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blmed.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = initApp()
api = Api(app)
CORS(app)


# Init Swagger
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='BLMed API',
        version='v0.1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/docs_json/',  # URI to access API Doc JSON
    'APISPEC_SWAGGER_UI_URL': '/docs/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

# Routs
# Service routs
api.add_resource(ServicesController, "/services")
docs.register(ServicesController)

api.add_resource(ServiceController,
                 "/service/<int:service_id>")
docs.register(ServiceController)
api.add_resource(ServiceSwitchController,
                 "/service/<int:service_id>/swap")
docs.register(ServiceSwitchController)

# Contact routs
api.add_resource(ContactController, "/contact")
docs.register(ContactController)

api.add_resource(ShowroomsController, "/contact/showroom")
docs.register(ShowroomsController)
api.add_resource(ShowroomController,
                 "/contact/showroom/<int:shoowroom_id>")
docs.register(ShowroomController)

# Category routs
api.add_resource(CategoriesController, "/category")
docs.register(CategoriesController)

api.add_resource(CategoryController,
                 "/category/<int:category_id>")
docs.register(CategoryController)

# Products routs
api.add_resource(ProductsController, "/products")
docs.register(ProductsController)

api.add_resource(ProductController, "/product/<int:product_id>")
docs.register(ProductController)

api.add_resource(ProductsByCategoryController,
                 "/products/category/<int:category_id>")
docs.register(ProductsByCategoryController)

api.add_resource(ProductsByFeaturedController,
                 "/products/featured")
docs.register(ProductsByFeaturedController)

api.add_resource(ProductsByLatestController,
                 "/products/latest")
docs.register(ProductsByLatestController)

# Upload images for product
api.add_resource(ImageController,
                 "/image")
docs.register(ImageController)
api.add_resource(ImageGetController,
                 "/image/<string:image_name>")
docs.register(ImageGetController)

if __name__ == "__main__":
    app.run(debug=True)
