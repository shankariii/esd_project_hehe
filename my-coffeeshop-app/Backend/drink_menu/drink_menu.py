from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flasgger import Swagger, swag_from
from os import environ

# Initialize Flask App
app = Flask(__name__)
CORS(app)

# Flasgger Swagger config
app.config['SWAGGER'] = {
    'title': 'Drink Menu Microservice API',
    'uiversion': 3
}
swagger = Swagger(app)

# MySQL Configuration using environment variable
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

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
        return {
            "drink_id": self.drink_id,
            "drink_name": self.drink_name,
            "description": self.description,
            "price": self.price,
            "image": self.image,
            "prep_time_min": self.prep_time_min
        }

@app.route('/')
def home():
    return jsonify({"message": "Coffee Ordering System API is running!"}), 200

@app.route('/drinks', methods=['GET'])
@app.route('/drinks/<int:drink_id>', methods=['GET'])
@swag_from({
    'responses': {
        200: {
            'description': 'List of drinks or a single drink by ID',
            'examples': {
                'application/json': [
                    {
                        "drink_id": 1,
                        "drink_name": "Latte",
                        "description": "Creamy coffee drink",
                        "price": 4.5,
                        "image": "latte.png",
                        "prep_time_min": 3
                    }
                ]
            }
        },
        404: {
            'description': 'Drink not found'
        }
    },
    'parameters': [
        {
            'name': 'drink_id',
            'in': 'path',
            'type': 'integer',
            'required': False,
            'description': 'ID of the drink to fetch'
        }
    ],
    'tags': ['Drink Menu']
})
def get_drinks(drink_id=None):
    if drink_id:
        drink = Drink.query.get(drink_id)
        if drink:
            return jsonify(drink.json()), 200
        return jsonify({"message": "Drink not found"}), 404

    drinks = Drink.query.all()
    return jsonify([d.json() for d in drinks]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)
