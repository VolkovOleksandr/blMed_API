from flask import Flask
from flask_restful import Api, Resource


app = Flask(__name__)
api = Api(app)


class Helo(Resource):
    def get(self):
        return {"data": "Hello"}


api.add_resource(Helo, "/helo")

if __name__ == "__main__":
    app.run(debug=True)
