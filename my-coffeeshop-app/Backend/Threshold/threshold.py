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

# Create Threshold table
class Threshold(db.Model):
    __tablename__ = 'threshold'

    threshold_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.Integer, nullable=False)
    ingredient = db.Column(db.String(255), primary_key=True, nullable=False)
    threshold = db.Column(db.DECIMAL(10, 2), nullable=False)
    safety_stock = db.Column(db.DECIMAL(10, 2), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Create a unique constraint for supplier_id and ingredient_id
    __table_args__ = (db.UniqueConstraint('supplier_id', 'ingredient', name='unique_supplier_ingredient'),)

    def __init__(self, supplier_id, ingredient, threshold, safety_stock):
        self.supplier_id = supplier_id
        self.ingredient = ingredient
        self.threshold = threshold
        self.safety_stock = safety_stock

    def __repr__(self):
        return f'<Threshold supplier_id={self.supplier_id} ingredient={self.ingredient}>'

    def json(self):
        return {
            "threshold_id": self.threshold_id,
            "supplier_id": self.supplier_id,
            "ingredient": self.ingredient,
            "threshold": float(self.threshold),
            "safety_stock": float(self.safety_stock),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

# GET all thresholds
@app.route("/threshold", methods=['GET'])
def get_all_thresholds():
    threshold_list = db.session.scalars(db.select(Threshold)).all()

    if threshold_list:
        return jsonify({
            "code": 200,
            "data": {
                "thresholds": [threshold.json() for threshold in threshold_list]
            }
        })
    
    return jsonify({
        "code": 404,
        "message": "No thresholds found."
    }), 404

# GET threshold by threshold ID
@app.route("/threshold/<int:threshold_id>", methods=['GET'])
def find_threshold_by_id(threshold_id):
    threshold = db.session.scalar(
        db.select(Threshold).filter_by(threshold_id=threshold_id)
    )

    if threshold:
        return jsonify({
            "code": 200,
            "data": threshold.json()
        })

    return jsonify({
        "code": 404,
        "message": "Threshold not found."
    }), 404

# GET supplier id by threshold id
@app.route("/threshold/<int:threshold_id>/supplier", methods=['GET'])
def find_supplier_id_by_threshold_id(threshold_id):
    threshold = db.session.scalar(
        db.select(Threshold).filter_by(threshold_id=threshold_id)
    )

    if threshold:
        return jsonify({
            "code": 200,
            "data": {
                "supplier_id": threshold.supplier_id
            }
        })

    return jsonify({
        "code": 404,
        "message": "Threshold not found."
    }), 404

# GET ingredient by threshold id
@app.route("/threshold/<int:threshold_id>/ingredient", methods=['GET'])
def find_ingredient_by_threshold_id(threshold_id):
    threshold = db.session.scalar(
        db.select(Threshold).filter_by(threshold_id=threshold_id)
    )

    if threshold:
        return jsonify({
            "code": 200,
            "data": {
                "ingredient": threshold.ingredient
            }
        })

    return jsonify({
        "code": 404,
        "message": "Threshold not found."
    }), 404

# GET safety stock by threshold id
@app.route("/threshold/<int:threshold_id>/safety-stock", methods=['GET'])
def find_safety_stock_by_threshold_id(threshold_id):
    threshold = db.session.scalar(
        db.select(Threshold).filter_by(threshold_id=threshold_id)
    )

    if threshold:
        return jsonify({
            "code": 200,
            "data": {
                "safety_stock": float(threshold.safety_stock)
            }
        })

    return jsonify({
        "code": 404,
        "message": "Threshold not found."
    }), 404

# GET thresholds by supplier ID
@app.route("/threshold/supplier/<int:supplier_id>", methods=['GET'])
def find_thresholds_by_supplier(supplier_id):
    thresholds = db.session.scalars(
        db.select(Threshold).filter_by(supplier_id=supplier_id)
    ).all()

    if thresholds:
        return jsonify({
            "code": 200,
            "data": {
                "thresholds": [threshold.json() for threshold in thresholds]
            }
        })

    return jsonify({
        "code": 404,
        "message": "No thresholds found for this supplier."
    }), 404

# GET threshold by ingredient
@app.route("/threshold/ingredient/<String:ingredient>", methods=['GET'])
def find_thresholds_by_ingredient(ingredient):
    thresholds = db.session.scalars(
        db.select(Threshold).filter_by(ingredient=ingredient)
    ).all()

    if thresholds:
        return jsonify({
            "code": 200,
            "data": {
                "thresholds": [threshold.json() for threshold in thresholds]
            }
        })

    return jsonify({
        "code": 404,
        "message": "No thresholds found for this ingredient."
    }), 404

# GET a specific threshold by supplier and ingredient
@app.route("/threshold/supplier/<int:supplier_id>/<String:ingredient>", methods=['GET'])
def find_threshold_by_supplier_and_ingredient(supplier_id, ingredient):
    threshold = db.session.scalar(
        db.select(Threshold).filter_by(supplier_id=supplier_id, ingredient=ingredient)
    )

    if threshold:
        return jsonify({
            "code": 200,
            "data": threshold.json()
        })

    return jsonify({
        "code": 404,
        "message": "Threshold not found for this supplier-ingredient combination."
    }), 404


# CREATE a new threshold
@app.route("/threshold", methods=['POST'])
def create_threshold():
    data = request.get_json()

    # Check for required fields
    if not all(key in data for key in ['supplier_id', 'ingredient', 'threshold', 'safety_stock']):
        return jsonify({
            "code": 400,
            "message": "Missing required fields."
        }), 400

    # Check if threshold already exists for this supplier-ingredient combination
    existing_threshold = db.session.scalar(
        db.select(Threshold).filter_by(
            supplier_id=data['supplier_id'],
            ingredient=data['ingredient']
        )
    )

    if existing_threshold:
        return jsonify({
            "code": 400,
            "message": "Threshold already exists for this supplier-ingredient combination."
        }), 400

    # Create new threshold
    threshold = Threshold(
        supplier_id=data['supplier_id'],
        ingredient=data['ingredient'],
        threshold=data['threshold'],
        safety_stock=data['safety_stock']
    )

    try:
        db.session.add(threshold)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred creating the threshold: {str(e)}"
        }), 500

    return jsonify({
        "code": 201,
        "data": threshold.json()
    }), 201

# UPDATE a threshold
@app.route("/threshold/<int:threshold_id>", methods=['PUT'])
def update_threshold(threshold_id):
    threshold = db.session.scalar(
        db.select(Threshold).filter_by(threshold_id=threshold_id)
    )

    if not threshold:
        return jsonify({
            "code": 404,
            "message": "Threshold not found."
        }), 404

    data = request.get_json()
    
    # Update fields if they exist in the request
    if 'threshold' in data:
        threshold.threshold = data['threshold']
    if 'safety_stock' in data:
        threshold.safety_stock = data['safety_stock']
    if 'supplier_id' in data:
        threshold.supplier_id = data['supplier_id']
    if 'ingredient' in data:
        threshold.ingredient = data['ingredient']

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred updating the threshold: {str(e)}"
        }), 500

    return jsonify({
        "code": 200,
        "data": threshold.json()
    })

# Update threshold by supplier and ingredients
@app.route("/threshold/supplier/<int:supplier_id>/<String:ingredient>", methods=['PUT'])
def update_threshold_by_supplier_and_ingredient(supplier_id, ingredient):
    threshold = db.session.scalar(
        db.select(Threshold).filter_by(supplier_id=supplier_id, ingredient=ingredient)
    )

    if not threshold:
        return jsonify({
            "code": 404,
            "message": "Threshold not found for this supplier-ingredient combination."
        }), 404

    data = request.get_json()
    
    # Update fields if they exist in the request
    if 'threshold' in data:
        threshold.threshold = data['threshold']
    if 'safety_stock' in data:
        threshold.safety_stock = data['safety_stock']

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred updating the threshold: {str(e)}"
        }), 500

    return jsonify({
        "code": 200,
        "data": threshold.json()
    })

# DELETE a threshold
@app.route("/threshold/<int:threshold_id>", methods=['DELETE'])
def delete_threshold(threshold_id):
    threshold = db.session.scalar(
        db.select(Threshold).filter_by(threshold_id=threshold_id)
    )

    if not threshold:
        return jsonify({
            "code": 404,
            "message": "Threshold not found."
        }), 404

    try:
        db.session.delete(threshold)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred deleting the threshold: {str(e)}"
        }), 500

    return jsonify({
        "code": 200,
        "message": "Threshold deleted successfully."
    })

# DELETE threshold by supplier and ingredient
@app.route("/threshold/supplier/<int:supplier_id>/<String:ingredient>", methods=['DELETE'])
def delete_threshold_by_supplier_and_ingredient(supplier_id, ingredient):
    threshold = db.session.scalar(
        db.select(Threshold).filter_by(supplier_id=supplier_id, ingredient=ingredient)
    )

    if not threshold:
        return jsonify({
            "code": 404,
            "message": "Threshold not found for this supplier-ingredient combination."
        }), 404

    try:
        db.session.delete(threshold)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred deleting the threshold: {str(e)}"
        }), 500

    return jsonify({
        "code": 200,
        "message": "Threshold deleted successfully."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8100, debug=True)