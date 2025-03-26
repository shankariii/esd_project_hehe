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
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/customisation'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@host.docker.internal:3306/drink_customisation'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db = SQLAlchemy(app)


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
# class CustomisationResource(Resource):
#     def get(self):
#         """Retrieve all customisations"""
#         customisations = Customisation.query.all()
#         return jsonify([customisation.json() for customisation in customisations])

# class CustomisationResource(Resource):
#     def get(self, customisation_id=None):
#         """Retrieve all customisations or a specific customisation"""
#         if customisation_id:
#             customisation = Customisation.query.get(customisation_id)
#             if customisation:
#                 return jsonify(customisation.json())
#             return jsonify({"message": "Customisation not found"}), 404

#         customisations = Customisation.query.all()
#         return jsonify([customisation.json() for customisation in customisations])
    
class CustomisationResource(Resource):
    def get(self, customisation_id=None):
        """Retrieve all customisations or a specific customisation"""
        if customisation_id:
            customisations = Customisation.query.filter_by(customisation_id=customisation_id).all()
            if customisations:
                return jsonify([customisation.json() for customisation in customisations])
            return jsonify({"message": "No customisations found"}), 404
        
        customisations = Customisation.query.all()
        return jsonify([customisation.json() for customisation in customisations])
    

class CustomisationByTypeResource(Resource):
    def get(self, customisation_type):
        """Retrieve customisations by type"""
        customisations = Customisation.query.filter_by(customisation_type=customisation_type).all()
        if customisations:
            return jsonify([customisations.json() for customisations in customisations])
        return jsonify({"message": "No customisations found for this type"}), 404


# Register API Endpoints
api.add_resource(CustomisationResource, '/customisations', '/customisations/<int:customisation_id>')
api.add_resource(CustomisationByTypeResource, '/customisations/type/<string:customisation_type>')


# Run App
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007, debug=True)
