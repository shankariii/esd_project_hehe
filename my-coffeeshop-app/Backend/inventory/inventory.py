from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

class Inventory(db.Model):
    __tablename__ = 'inventory'

    inventory_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient = db.Column(db.String(64), nullable=False)
    available_quantity = db.Column(db.Float(precision=2), nullable=False)
    unit = db.Column(db.String(32), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)
    change_in_quantity = db.Column(db.Float(precision=2), default=0.0)

    def __init__(self, ingredient, available_quantity, unit, change_in_quantity=0.0):
        self.ingredient = ingredient
        self.available_quantity = available_quantity
        self.unit = unit
        self.date_time = datetime.utcnow()
        self.change_in_quantity = change_in_quantity

    def json(self):
        return {
            "inventory_id": self.inventory_id,
            "ingredient": self.ingredient,
            "available_quantity": self.available_quantity,
            "unit": self.unit,
            "date_time": self.date_time.strftime('%Y-%m-%d %H:%M:%S'),
            "change_in_quantity": self.change_in_quantity
        }

@app.route("/inventory")
def get_all_items():
    item_list = db.session.scalars(db.select(Inventory)).all()
    if item_list:
        return jsonify({
            "code": 200,
            "data": {
                "inventory": [item.json() for item in item_list]
            }
        })
    return jsonify({"code": 404, "message": "No inventory items found."}), 404

@app.route("/inventory/<int:inventory_id>")
def get_item_by_id(inventory_id):
    item = db.session.scalar(db.select(Inventory).filter_by(inventory_id=inventory_id))
    if item:
        return jsonify({"code": 200, "data": item.json()})
    return jsonify({"code": 404, "message": "Inventory item not found."}), 404

#for scenario 3: get by ingredient id 
@app.route("/inventory/ingredient/<string:ingredient>", methods=["GET"])
def get_item_by_ingredient(ingredient):
    item = db.session.scalar(db.select(Inventory).filter_by(ingredient=ingredient))
    if item:
        return jsonify({"code": 200, "data": item.json()})
    return jsonify({"code": 404, "message": f"Inventory item with ingredient '{ingredient}' not found."}), 404

@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json()
    required = ['ingredient', 'available_quantity', 'unit']
    if not all(key in data for key in required):
        return jsonify({"code": 400, "message": "Missing required fields."}), 400

    change = data.get('change_in_quantity', data['available_quantity'])

    item = Inventory(
        ingredient=data['ingredient'],
        available_quantity=data['available_quantity'],
        unit=data['unit'],
        change_in_quantity=change
    )
    try:
        db.session.add(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "An error occurred creating the item.", "error": str(e)}), 500

    return jsonify({"code": 201, "data": item.json()}), 201

@app.route("/inventory/<int:inventory_id>", methods=["PUT"])
def update_item(inventory_id):
    item = db.session.scalar(db.select(Inventory).filter_by(inventory_id=inventory_id))
    if not item:
        return jsonify({"code": 404, "message": "Item not found."}), 404

    data = request.get_json()
    try:
        new_quantity = data.get("available_quantity", item.available_quantity)
        change = new_quantity - item.available_quantity

        item.ingredient = data.get("ingredient", item.ingredient)
        item.available_quantity = new_quantity
        item.unit = data.get("unit", item.unit)
        item.date_time = datetime.utcnow()
        item.change_in_quantity = change

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "An error occurred updating the item.", "error": str(e)}), 500

    return jsonify({"code": 200, "data": item.json()})

@app.route("/inventory/<int:inventory_id>", methods=["DELETE"])
def delete_item(inventory_id):
    item = db.session.scalar(db.select(Inventory).filter_by(inventory_id=inventory_id))
    if not item:
        return jsonify({"code": 404, "message": "Item not found."}), 404

    try:
        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"code": 500, "message": "Failed to delete item.", "error": str(e)}), 500

    return jsonify({"code": 200, "message": "Item deleted successfully."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)