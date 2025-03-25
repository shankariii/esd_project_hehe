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
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/drink_ingredients'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@host.docker.internal:3306/drink_ingredients'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)


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
    

@app.route('/')
def home():
    return jsonify({"message": "Coffee Ordering System API is running!"}), 200


# API Resources
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


# Register API Endpoints
api.add_resource(DrinkIngredientResource, '/ingredients', '/ingredients/<int:drink_id>')


# Run App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5006, debug=True)
