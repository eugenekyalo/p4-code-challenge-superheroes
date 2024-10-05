#!/usr/bin/env python3

from flask import Flask, request, jsonify
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Hero, Power, HeroPower
import os

# Define base directory and database URI
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# Initialize the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Set up database migration
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Flask-RESTful API
api = Api(app)

# Route for the homepage
@app.route('/')
def index():
    return '<h1>Superheroes Code Challenge</h1>'

# HeroResource: GET all heroes, POST a new hero
class HeroResource(Resource):
    def get(self):
        heroes = Hero.query.all()
        hero_list = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
        return jsonify(hero_list)

    def post(self):
        data = request.get_json()
        new_hero = Hero(name=data['name'], super_name=data['super_name'])
        db.session.add(new_hero)
        db.session.commit()
        return {"message": "Hero created successfully!"}, 201

# PowerResource: GET all powers, POST a new power
class PowerResource(Resource):
    def get(self):
        powers = Power.query.all()
        power_list = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
        return jsonify(power_list)

    def post(self):
        data = request.get_json()
        new_power = Power(name=data['name'], description=data['description'])
        db.session.add(new_power)
        db.session.commit()
        return {"message": "Power created successfully!"}, 201

# HeroPowerResource: POST to assign power to a hero
class HeroPowerResource(Resource):
    def post(self):
        data = request.get_json()
        new_hero_power = HeroPower(hero_id=data['hero_id'], power_id=data['power_id'], strength=data['strength'])
        db.session.add(new_hero_power)
        db.session.commit()
        return {"message": "Power assigned to hero successfully!"}, 201

# Register the resources and routes with the API
api.add_resource(HeroResource, '/heroes')
api.add_resource(PowerResource, '/powers')
api.add_resource(HeroPowerResource, '/hero_powers')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
