from flask import Flask
from flask_restful import Api
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

from models.db import db

from controllers.services_controller import ServicesController
from controllers.service_controller import ServiceController
from controllers.service_swich_controller import ServiceSwitchController
from controllers.contact_controller import ContactController
from controllers.showrooms_controller import ShowroomsController
from controllers.showroom_controller import ShowroomController
from controllers.categories_controller import CategoriesController
from controllers.category_controller import CategoryController
from controllers.products_controller import ProductsController
from controllers.products_by_category_controller import ProductsByCategoryController
from controllers.product_by_featured import ProductsByFeaturedController

# init app


def initApp():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blmed.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = initApp()
api = Api(app)


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

api.add_resource(ProductsByCategoryController,
                 "/products/category/<int:category_id>")
docs.register(ProductsByCategoryController)

api.add_resource(ProductsByFeaturedController,
                 "/products/featured")
docs.register(ProductsByFeaturedController)

if __name__ == "__main__":
    app.run(debug=True)
