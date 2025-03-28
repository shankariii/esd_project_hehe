from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from flasgger import Swagger

app = Flask(__name__)
CORS(app)
Swagger(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')  # Set this in your .env or environment
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

# Outlet model
class Outlet(db.Model):
    __tablename__ = 'outlets'

    outlet_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.Text, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    contact_info = db.Column(db.String(20), nullable=False)  # Phone number

    def json(self):
        return {
            "id": self.outlet_id,
            "name": self.name,
            "address": self.address,
            "position": {
                "lat": self.latitude,
                "lng": self.longitude
            },
            "queueCount": 0  # Placeholder value; integrate real data later if needed
        }

@app.route("/")
def index():
    return jsonify({"message": "Outlet microservice is running"}), 200

@app.route("/outlets", methods=["GET"])
def get_all_outlets():
    """
    Get all outlets or filter by name
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: false
        description: Partial name match
    responses:
      200:
        description: List of outlets
    """
    name_filter = request.args.get("name")
    if name_filter:
        outlets = Outlet.query.filter(Outlet.name.ilike(f"%{name_filter}%")).all()
    else:
        outlets = Outlet.query.all()

    return jsonify([o.json() for o in outlets]), 200

@app.route("/outlets/<int:outlet_id>", methods=["GET"])
def get_outlet_by_id(outlet_id):
    """
    Get outlet by ID
    ---
    parameters:
      - name: outlet_id
        in: path
        type: integer
        required: true
        description: ID of the outlet
    responses:
      200:
        description: Outlet found
      404:
        description: Outlet not found
    """
    outlet = Outlet.query.get(outlet_id)
    if outlet:
        return jsonify(outlet.json()), 200
    else:
        return jsonify({"error": "Outlet not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
