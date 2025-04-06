from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger
from os import environ

# Initialize Flask App
app = Flask(__name__)
CORS(app)
Swagger(app)  # Enable Swagger UI

# MySQL Configuration using environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

# Initialize DB
db = SQLAlchemy(app)

# Define Drink Ingredients Model
class DrinkIngredient(db.Model):
    __tablename__ = 'drink_ingredients'

    drink_ingredient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    drink_id = db.Column(db.Integer, db.ForeignKey('drink_menu.drink_id'), nullable=False)
    ingredient = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.String(15), nullable=False)

    def json(self):
        return {
            "drink_ingredient_id": self.drink_ingredient_id,
            "drink_id": self.drink_id,
            "ingredient": self.ingredient,
            "quantity": self.quantity,
            "unit": self.unit
        }

@app.route('/')
def index():
    """Health check endpoint
    ---
    responses:
      200:
        description: Returns a message if service is running
    """
    return jsonify({"message": "Drink Ingredients microservice is running!"}), 200

@app.route('/ingredients', methods=['GET'])
@app.route('/ingredients/<int:drink_id>', methods=['GET'])
def get_ingredients(drink_id=None):
    """
    Get all drink ingredients or filter by drink_id
    ---
    parameters:
      - name: drink_id
        in: path
        type: integer
        required: false
        description: ID of the drink to filter ingredients
    responses:
      200:
        description: List of ingredients
      404:
        description: No ingredients found
    """
    if drink_id:
        ingredients = DrinkIngredient.query.filter_by(drink_id=drink_id).all()
        if ingredients:
            return jsonify([i.json() for i in ingredients]), 200
        return jsonify({"message": "No ingredients found for this drink"}), 404

    ingredients = DrinkIngredient.query.all()
    return jsonify([i.json() for i in ingredients]), 200


@app.route('/ingredients/DIID/<int:drink_ingredient_id>', methods=['GET'])
def get_ingredient_by_id(drink_ingredient_id):
    """
    Get a specific drink ingredient by its ID
    ---
    parameters:
      - name: drink_ingredient_id
        in: path
        type: integer
        required: true
        description: ID of the drink ingredient
    responses:
      200:
        description: Drink ingredient details
      404:
        description: Ingredient not found
    """
    ingredient = DrinkIngredient.query.filter_by(drink_ingredient_id=drink_ingredient_id).first()
    if ingredient:
        return jsonify(ingredient.json()), 200
    return jsonify({"message": "Ingredient not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5006)
