from flask import Flask
from flask_restful import Api
from models.db import db


from controllers.services_controller import ServicesController
from controllers.service_controller import ServiceController


# init app
def initApp():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blmed.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = initApp()
api = Api(app)

# Routs
api.add_resource(ServicesController, "/services")
api.add_resource(ServiceController,
                 "/service/<int:service_id>")

if __name__ == "__main__":
    app.run(debug=True)
