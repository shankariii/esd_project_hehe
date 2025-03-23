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

# MySQL Configuration (Using Docker Environment Variables)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/drink'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@host.docker.internal:3306/drink'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

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

# Define Drink Ingredients Model
class DrinkIngredient(db.Model):
    __tablename__ = 'drink_ingredients'

    drink_ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink_menu.drink_id'), nullable=False)
    ingredient_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(15), nullable=False)

    def json(self):
        return {
            "drink_ingredient_id": self.drink_ingredient_id,
            "drink_id": self.drink_id,
            "ingredient_id": self.ingredient_id,
            "quantity": self.quantity,
            "unit": self.unit
        }

# Define Customisation Model
class Customisation(db.Model):
    __tablename__ = 'customisation'

    customisation_id = db.Column(db.Integer, primary_key=True)
    customisation_type = db.Column(db.String(10), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    price_diff = db.Column(db.Float, nullable=False)

    def json(self):
        return {
            "customisation_id": self.customisation_id,
            "customisation_type": self.customisation_type,
            "name": self.name,
            "price_diff": self.price_diff
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

class DrinkIngredientResource(Resource):
    def get(self, drink_id=None):
        """Retrieve all drink ingredients or filter by drink_id"""
        if drink_id:
            ingredients = DrinkIngredient.query.filter_by(drink_id=drink_id).all()
            if ingredients:
                return jsonify([ingredient.json() for ingredient in ingredients])
            return jsonify({"message": "No ingredients found for this drink"}), 404
        
        ingredients = DrinkIngredient.query.all()
        return jsonify([ingredient.json() for ingredient in ingredients])

class CustomisationResource(Resource):
    def get(self):
        """Retrieve all customisations"""
        customisations = Customisation.query.all()
        return jsonify([customisation.json() for customisation in customisations])

class CustomisationResource(Resource):
    def get(self, customisation_id=None):
        """Retrieve all customisations or a specific customisation"""
        if customisation_id:
            customisation = Customisation.query.get(customisation_id)
            if customisation:
                return jsonify(customisation.json())
            return jsonify({"message": "Customisation not found"}), 404

        customisations = Customisation.query.all()
        return jsonify([customisation.json() for customisation in customisations])


# Register API Endpoints
api.add_resource(DrinkResource, '/drinks', '/drinks/<int:drink_id>')
api.add_resource(DrinkIngredientResource, '/ingredients', '/ingredients/<int:drink_id>')
api.add_resource(CustomisationResource, '/customisations', '/customisations/<int:customisation_id>')


# Run App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
