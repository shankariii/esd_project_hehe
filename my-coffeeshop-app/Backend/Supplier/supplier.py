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

# Create Supplier table
class Supplier(db.Model):
    __tablename__ = 'supplier'

    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    contact_person = db.Column(db.String(255))
    phone = db.Column(db.String(8))
    email = db.Column(db.String(255), unique=True)
    address = db.Column(db.Text)
    created_at = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    updated_at = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, name, contact_person=None, phone=None, email=None, address=None):
        self.name = name
        self.contact_person = contact_person
        self.phone = phone
        self.email = email
        self.address = address

    def __repr__(self):
        return f'<Supplier {self.name}>'

    def json(self):
        return {
            "supplier_id": self.supplier_id,
            "name": self.name,
            "contact_person": self.contact_person,
            "phone": self.phone,
            "email": self.email,
            "address": self.address,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }

# Routes for Supplier

# GET all suppliers
@app.route("/supplier", methods=['GET'])
def get_all_suppliers():
    supplier_list = db.session.scalars(db.select(Supplier)).all()

    if supplier_list:
        return jsonify({
            "code": 200,
            "data": {
                "suppliers": [supplier.json() for supplier in supplier_list]
            }
        })
    
    return jsonify({
        "code": 404,
        "message": "No suppliers found."
    }), 404

# GET a supplier by ID
@app.route("/supplier/<int:supplier_id>", methods=['GET'])
def find_supplier_by_id(supplier_id):
    supplier = db.session.scalar(
        db.select(Supplier).filter_by(supplier_id=supplier_id)
    )

    if supplier:
        return jsonify({
            "code": 200,
            "data": supplier.json()
        })

    return jsonify({
        "code": 404,
        "message": "Supplier not found."
    }), 404

# GET the supplier's name by supplier ID
@app.route("/supplier/<int:supplier_id>/name", methods=['GET'])
def find_supplier_name_by_id(supplier_id):
    supplier = db.session.scalar(
        db.select(Supplier).filter_by(supplier_id=supplier_id)
    )
    if supplier:
        return jsonify({
            "code": 200,
            "data": {"name": supplier.name}
        })
    
    return jsonify({
        "code": 404,
        "message": "Supplier name not found."
    }), 404

# GET contact person by supplier ID
@app.route("/supplier/<int:supplier_id>/contact_person", methods=['GET'])
def find_supplier_contact_person_by_id(supplier_id):
    supplier = db.session.scalar(
        db.select(Supplier).filter_by(supplier_id=supplier_id)
    )
    if supplier:
        return jsonify({
            "code": 200,
            "data": {"contact_person": supplier.contact_person}
        })
    return jsonify({
        "code": 404,
        "message": "Supplier contact person not found."
    }), 404

# GET phone number by supplier ID
@app.route("/supplier/<int:supplier_id>/phone", methods=['GET'])
def find_supplier_phone_by_id(supplier_id):
    supplier = db.session.scalar(
        db.select(Supplier).filter_by(supplier_id=supplier_id)
    )
    if supplier:
        return jsonify({
            "code": 200,
            "data": {"phone": supplier.phone}
        })
    return jsonify({
        "code": 404,
        "message": "Supplier phone number not found."
    }), 404

# GET email by supplier ID
@app.route("/supplier/<int:supplier_id>/email", methods=['GET'])
def find_supplier_email_by_id(supplier_id):
    supplier = db.session.scalar(
        db.select(Supplier).filter_by(supplier_id=supplier_id)
    )
    if supplier:
        return jsonify({
            "code": 200,
            "data": {"email": supplier.email}
        })
    return jsonify({
        "code": 404,
        "message": "Supplier email not found."
    }), 404

# GET address by supplier ID
@app.route("/supplier/<int:supplier_id>/address", methods=['GET'])
def find_supplier_address_by_id(supplier_id):
    supplier = db.session.scalar(
        db.select(Supplier).filter_by(supplier_id=supplier_id)
    )
    if supplier:
        return jsonify({
            "code": 200,
            "data": {"address": supplier.address}
        })
    return jsonify({
        "code": 404,
        "message": "Supplier address not found."
    }), 404

# CREATE a new supplier
@app.route("/supplier", methods=['POST'])
def create_supplier():
    data = request.get_json()

    if db.session.scalar(db.select(Supplier).filter_by(email=data.get("email"))):
        return jsonify({
            "code": 400,
            "message": "Supplier with this email already exists."
        }), 400

    supplier = Supplier(**data)

    try:
        db.session.add(supplier)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred while creating the supplier: {str(e)}"
        }), 500

    return jsonify({
        "code": 201,
        "data": supplier.json()
    }), 201

# UPDATE a supplier's information
@app.route("/supplier/<int:supplier_id>", methods=['PUT'])
def update_supplier(supplier_id):
    supplier = db.session.scalar(
        db.select(Supplier).filter_by(supplier_id=supplier_id)
    )

    if not supplier:
        return jsonify({
            "code": 404,
            "message": "Supplier not found."
        }), 404

    data = request.get_json()
    for key, value in data.items():
        setattr(supplier, key, value)

    try:
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred while updating the supplier: {str(e)}"
        }), 500

    return jsonify({
        "code": 200,
        "data": supplier.json()
    })

# DELETE a supplier
@app.route("/supplier/<int:supplier_id>", methods=['DELETE'])
def delete_supplier(supplier_id):
    supplier = db.session.scalar(
        db.select(Supplier).filter_by(supplier_id=supplier_id)
    )

    if not supplier:
        return jsonify({
            "code": 404,
            "message": "Supplier not found."
        }), 404

    try:
        db.session.delete(supplier)
        db.session.commit()
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"An error occurred while deleting the supplier: {str(e)}"
        }), 500

    return jsonify({
        "code": 200,
        "message": "Supplier deleted successfully."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8200, debug=True)