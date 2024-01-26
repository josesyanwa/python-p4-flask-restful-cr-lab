from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource, reqparse
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

class PlantByID(Resource):
    def get(self, plant_id):
        plant = Plant.query.get_or_404(plant_id)
        return jsonify(plant.to_dict())

class CreatePlant(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, required=True, help='Name cannot be blank')
        self.reqparse.add_argument('image', type=str, required=True, help='Image cannot be blank')
        self.reqparse.add_argument('price', type=float, required=True, help='Price cannot be blank')

    def post(self):
        args = self.reqparse.parse_args()
        new_plant = Plant(**args)
        db.session.add(new_plant)
        db.session.commit()
        return jsonify(new_plant.to_dict()), 201

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:plant_id>')
api.add_resource(CreatePlant, '/plants/create')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
