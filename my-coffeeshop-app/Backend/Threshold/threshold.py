from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ
from prometheus_client import Gauge, generate_latest, CONTENT_TYPE_LATEST

app = Flask(__name__)
CORS(app)

# metrics = PrometheusMetrics(app)

app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

# Prometheus Gauge to track threshold values per ingredient
threshold_gauge = Gauge('threshold_value', 'Threshold value of ingredients', ['ingredient'])

# Create Threshold table
class Threshold(db.Model):
    __tablename__ = 'threshold'

    threshold_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ingredient = db.Column(db.String(255), nullable=False, unique = True)
    threshold = db.Column(db.DECIMAL(10, 2), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, ingredient, threshold):
        self.ingredient = ingredient
        self.threshold = threshold

    def __repr__(self):
        return f'<Threshold ingredient={self.ingredient}>'

    def json(self):
        return {
            "threshold_id": self.threshold_id,
            "ingredient": self.ingredient,
            "threshold": float(self.threshold),
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

# GET threshold by ingredient
@app.route("/threshold/ingredient/<string:ingredient>", methods=['GET'])
def find_thresholds_by_ingredient(ingredient):
    threshold = db.session.scalar(
        db.select(Threshold).filter_by(ingredient=ingredient)
    )

    if threshold:
        return jsonify({
            "code": 200,
            "data":  threshold.json()
        })

    return jsonify({
        "code": 404,
        "message": "No thresholds found for this ingredient."
    }), 404

# CREATE a new threshold
@app.route("/threshold", methods=['POST'])
def create_threshold():
    data = request.get_json()

    # Check for required fields
    if not all(key in data for key in ['ingredient', 'threshold']):
        return jsonify({
            "code": 400,
            "message": "Missing required fields."
        }), 400

    ingredient = data['ingredient']

    # Check if threshold already exists for this ingredient
    existing_threshold = db.session.scalar(
        db.select(Threshold).filter_by(
            ingredient=ingredient)
        )

    if existing_threshold:
        return jsonify({
            "code": 400,
            "message": "Threshold already exists for this ingredient."
        }), 400

    # if no threshold for the ingredient, create threshold
    threshold = Threshold(
        ingredient=data['ingredient'],
        threshold=data['threshold']
    )

    try:
        db.session.add(threshold)
        db.session.commit()
        return jsonify({
        "code": 201,
        "data": threshold.json()
    }), 201
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred creating the threshold: {str(e)}"
        }), 500

# UPDATE a threshold
@app.route("/threshold/<int:threshold_id>", methods=['PUT'])
def update_threshold(threshold_id):
    threshold = db.session.scalar(
        db.select(Threshold).filter_by(threshold_id=threshold_id)
    )

    if not threshold: #if no current threshold record with specified threshold_id
        return jsonify({
            "code": 404,
            "message": f"Cannot update threshold. Threshold with ID:{threshold_id} not found."
        }), 404

    data = request.get_json()
    
    # Update fields if they exist in the request
    if 'threshold' in data:
        threshold.threshold = data['threshold']

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
            "message": f"Cannot delete threshold. Threshold with ID:{threshold_id} not found."
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

def refresh_threshold_metrics():
    """Fetch all thresholds and update the Prometheus gauge."""
    threshold_list = db.session.scalars(db.select(Threshold)).all()
    threshold_gauge.clear()  # Clear previous values to avoid duplicates
    for threshold in threshold_list:
        threshold_gauge.labels(ingredient=threshold.ingredient).set(float(threshold.threshold))

@app.route("/metrics")
def metrics():
    """Expose Prometheus metrics, including custom thresholds."""
    # Refresh threshold metrics before returning
    refresh_threshold_metrics()
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8100, debug=True)
    app.run(host='0.0.0.0', port=8100, debug=False)