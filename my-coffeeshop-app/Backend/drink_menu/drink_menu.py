from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
import pymysql
import os
from os import environ
from flask_cors import CORS


# Initialize Flask App
app = Flask(__name__)
api = Api(app)
CORS(app)

# MySQL Configuration (Using Docker Environment Variables)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/drink_menu'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@host.docker.internal:3306/drink_menu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)

# Define Drink Model
class Drink(db.Model):
    __tablename__ = 'drink_menu'

    drink_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    drink_name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(255), nullable=True)
    prep_time_min = db.Column(db.Float, nullable=False)

    def json(self):
        # Ensure that the image is a valid string and handle cases where it's None
        # image_url = self.image if isinstance(self.image, str) else "default_image_path.jpg"
        return {
            "drink_id": self.drink_id,
            "drink_name": self.drink_name,
            "description": self.description,
            "price": self.price,
            "image": self.image,  # Ensure image is a valid string
            "prep_time_min": self.prep_time_min
        }


@app.route('/')
def home():
    return jsonify({"message": "Coffee Ordering System API is running!"}), 200


# API Resources
class DrinkResource(Resource):
    def get(self, drink_id=None):
        """Retrieve all drinks or a specific drink"""
        if drink_id:
            drink = Drink.query.get(drink_id)
            if drink:
                return jsonify(drink.json())
            return jsonify({"message": "Drink not found"}), 404

        drinks = Drink.query.all()
        return jsonify([drink.json() for drink in drinks])


# Register API Endpoints
api.add_resource(DrinkResource, '/drinks', '/drinks/<int:drink_id>')


# Run App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
