from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ

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
    ingredient_id = db.Column(db.String(64), nullable=False)
    available_quantity = db.Column(db.Float(precision=2), nullable=False)
    unit = db.Column(db.String(32), nullable=False)

    def __init__(self, ingredient_id, available_quantity, unit):
        self.ingredient_id = ingredient_id
        self.available_quantity = available_quantity
        self.unit = unit

    def json(self):
        return {
            "inventory_id": self.inventory_id,
            "ingredient_id": self.ingredient_id,
            "available_quantity": self.available_quantity,
            "unit": self.unit
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
@app.route("/inventory/ingredient/<string:ingredient_id>", methods=["GET"])
def get_item_by_ingredient_id(ingredient_id):
    item = db.session.scalar(db.select(Inventory).filter_by(ingredient_id=ingredient_id))
    if item:
        return jsonify({"code": 200, "data": item.json()})
    return jsonify({"code": 404, "message": f"Inventory item with ingredient_id '{ingredient_id}' not found."}), 404


@app.route("/inventory", methods=["POST"])
def create_item():
    data = request.get_json()
    required = ['ingredient_id', 'available_quantity', 'unit']
    if not all(key in data for key in required):
        return jsonify({"code": 400, "message": "Missing required fields."}), 400

    item = Inventory(**data)
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
        item.ingredient_id = data.get("ingredient_id", item.ingredient_id)
        item.available_quantity = data.get("available_quantity", item.available_quantity)
        item.unit = data.get("unit", item.unit)
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
