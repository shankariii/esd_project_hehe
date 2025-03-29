from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

# Create SupplierIngredient table
class SupplierIngredient(db.Model):
    __tablename__ = 'supplier_ingredient'

    ingredient = db.Column(db.String(100), primary_key=True, nullable=False)
    supplier_id = db.Column(db.Integer, nullable=False)
    price_per_unit = db.Column(db.DECIMAL(10, 2), nullable=False)
    lead_time = db.Column(db.Integer, nullable=False)
    last_updated = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, ingredient, supplier_id, price_per_unit, lead_time):
        self.ingredient = ingredient
        self.supplier_id = supplier_id
        self.price_per_unit = price_per_unit
        self.lead_time = lead_time

    def json(self):
        return {
            "ingredient": self.ingredient,
            "supplier_id": self.supplier_id,
            "price_per_unit": float(self.price_per_unit),
            "lead_time": self.lead_time,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }

    def __repr__(self):
        return f'<SupplierIngredient ingredient={self.ingredient} supplier_id={self.supplier_id}>'

# Routes for SupplierIngredient

# GET all supplier-ingredient relationships
@app.route("/supplier_ingredient", methods=['GET'])
def get_all_supplier_ingredients():
    supplier_ingredient_list = db.session.scalars(db.select(SupplierIngredient)).all()

    if supplier_ingredient_list:
        return jsonify({
            "code": 200,
            "data": {
                "supplier_ingredients": [entry.json() for entry in supplier_ingredient_list]
            }
        })

    return jsonify({
        "code": 404,
        "message": "No supplier-ingredient relationships found."
    }), 404

# GET the supplier id for an ingredient
@app.route("/supplier_ingredient/ingredient/<string:ingredient>/supplier", methods=['GET'])
def get_supplier_by_ingredient(ingredient):
    supplier_ingredient = db.session.scalar(
        db.select(SupplierIngredient).filter_by(ingredient=ingredient)
    )

    if supplier_ingredient:
         return jsonify({
                "code": 200,
                "data": {"supplier_id": supplier_ingredient.supplier_id}
            })

    return jsonify({
        "code": 404,
        "message": "Supplier-ingredient relationship not found."
    }), 404
    
# GET the price_per_unit for an ingredient
@app.route("/supplier_ingredient/ingredient/<string:ingredient>/price", methods=['GET'])
def get_price_by_ingredient(ingredient):
    supplier_ingredient = db.session.scalar(
        db.select(SupplierIngredient).filter_by(ingredient=ingredient)
    )
    if supplier_ingredient:
        return jsonify({
            "code": 200,
            "data": {"price_per_unit": float(supplier_ingredient.price_per_unit)}
        })
    
    return jsonify({
        "code": 404,
        "message": "Price per unit not found for this ingredient."
    }), 404

# GET the lead_time for an ingredient
@app.route("/supplier_ingredient/ingredient/<string:ingredient>/lead_time", methods=['GET'])
def get_lead_time_by_ingredient(ingredient):
    supplier_ingredient = db.session.scalar(
        db.select(SupplierIngredient).filter_by(ingredient=ingredient)
    )
    if supplier_ingredient:
        return jsonify({
            "code": 200,
            "data": {"lead_time": supplier_ingredient.lead_time}
        })
    
    return jsonify({
        "code": 404,
        "message": "Lead time not found for this ingredient."
    }), 404

# GET all ingredients for a specific supplier
@app.route("/supplier_ingredient/supplier/<int:supplier_id>/ingredients", methods=['GET'])
def get_ingredients_by_supplier(supplier_id):
    supplier_ingredients = db.session.scalars(
        db.select(SupplierIngredient).filter_by(supplier_id=supplier_id)
    ).all()

    if supplier_ingredients:
        return jsonify({
            "code": 200,
            "data": {
                "supplier_ingredients": [entry.json() for entry in supplier_ingredients]
            }
        })

    return jsonify({
        "code": 404,
        "message": "No ingredients found for this supplier."
    }), 404

# CREATE a new supplier-ingredient relationship
@app.route("/supplier_ingredient", methods=['POST'])
def create_supplier_ingredient():
    data = request.get_json()

    if not data.get("supplier_id") or not data.get("ingredient"):
        return jsonify({
            "code": 400,
            "message": "Supplier ID and Ingredient are required."
        }), 400
    
    existing_ingredient = db.session.scalar(
        db.select(SupplierIngredient).filter_by(
            ingredient=data.get("ingredient")
        )
    )

    if existing_ingredient:
        return jsonify({
            "code": 400,
            "message": "This ingredient already has a supplier. An ingredient can only have one supplier."
        }), 400

    supplier_ingredient = SupplierIngredient(**data)

    try:
        db.session.add(supplier_ingredient)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred while creating the supplier-ingredient relationship: {str(e)}"
        }), 500

    return jsonify({
        "code": 201,
        "data": supplier_ingredient.json()
    }), 201

# UPDATE a supplier-ingredient relationship
@app.route("/supplier_ingredient/<string:ingredient>", methods=['PUT'])
def update_supplier_ingredient(ingredient):
    supplier_ingredient = db.session.scalar(
        db.select(SupplierIngredient).filter_by(ingredient=ingredient)
    )

    if not supplier_ingredient:
        return jsonify({
            "code": 404,
            "message": "Supplier-ingredient relationship not found."
        }), 404

    data = request.get_json()
    if "supplier_id" in data:
        supplier_ingredient.supplier_id = data["supplier_id"]
    if "price_per_unit" in data:
        supplier_ingredient.price_per_unit = data["price_per_unit"]
    if "lead_time" in data:
        supplier_ingredient.lead_time = data["lead_time"]

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred while updating the supplier-ingredient relationship: {str(e)}"
        }), 500

    return jsonify({
        "code": 200,
        "data": supplier_ingredient.json(),
        "message": "Supplier-ingredient relationship updated successfully."
    })

# DELETE a supplier-ingredient relationship
@app.route("/supplier_ingredient", methods=['DELETE'])
def delete_supplier_ingredient():

    data = request.get_json()

    if 'ingredient' not in data:
        return jsonify({
            "code": 400,
            "message": "Ingredient is required in the request body."
        }), 400

    ingredient = data['ingredient']
    
    supplier_ingredient = db.session.scalar(
        db.select(SupplierIngredient).filter_by(ingredient=ingredient)
    )

    if not supplier_ingredient:
        return jsonify({
            "code": 404,
            "message": "Supplier-ingredient relationship not found."
        }), 404

    try:
        db.session.delete(supplier_ingredient)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred while deleting the supplier-ingredient relationship: {str(e)}"
        }), 500

    return jsonify({
        "code": 200,
        "message": "Supplier-ingredient relationship deleted successfully."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001, debug=True)