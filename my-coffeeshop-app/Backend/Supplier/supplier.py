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

#Create Supplier table
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

    def __repr__(self): #for debugging and displaying Supplier objects
            return f'<Supplier {self.name}>' 

    def json(self):
            return {
                "supplier_id": self.supplier_id,
                "name": self.name,
                "contact_person": self.contact_person,
                "phone": self.phone,
                "email": self.email,
                "address": self.address,
                "created_at": self.created_at.isoformat() if self.created_at else None,  # Handle potential None values
                "updated_at": self.updated_at.isoformat() if self.updated_at else None   # Handle potential None values
            }

#Create Supplier_Ingredient table
class SupplierIngredient(db.Model):
    __tablename__ = 'supplier_ingredient'

   
    ingredient_id = db.Column(db.Integer, nullable=False, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.supplier_id', ondelete='CASCADE'), nullable=False)
    price_per_unit = db.Column(db.DECIMAL(10, 2), nullable=False)
    lead_time = db.Column(db.Integer, nullable = False)
    last_updated = db.Column(db.TIMESTAMP, default=datetime.utcnow, onupdate=datetime.utcnow)

    supplier = db.relationship('Supplier', backref=db.backref('supplier_ingredient', lazy=True))

    def __init__(self, ingredient_id, supplier_id, price_per_unit, lead_time):
        self.ingredient_id = ingredient_id
        self.supplier_id = supplier_id
        self.price_per_unit = price_per_unit
        self.lead_time = lead_time

    def json(self):
        return {
           
            "ingredient_id": self.ingredient_id,
            "supplier_id": self.supplier_id,
            "price_per_unit": float(self.price_per_unit),
            "lead_time": self.lead_time,
            "last_updated": self.last_updated.isoformat() if self.last_updated else None
        }

    def __repr__(self):
        return f'<SupplierIngredient ingredient_id={self.ingredient_id} supplier_id={self.supplier_id}>'
    

    
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

# GET a supplier's name by supplier ID
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


# GET a supplier's contact person by supplier ID
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

# GET a supplier's phone number by supplier ID
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

# GET a supplier's email by supplier ID
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

# GET a supplier's address by supplier ID
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

# GET the supplier for an ingredient
@app.route("/supplier_ingredient/ingredient/<int:ingredient_id>/supplier", methods=['GET'])
def get_supplier_by_ingredient(ingredient_id):
    supplier_ingredient = db.session.scalar(
        db.select(SupplierIngredient).filter_by(ingredient_id=ingredient_id)
    )

    if supplier_ingredient:
        supplier = db.session.scalar(
            db.select(Supplier).filter_by(supplier_id=supplier_ingredient.supplier_id)
        )
        
        if supplier:
            return jsonify({
                "code": 200,
                "data": {"supplier": supplier.json()}
            })

        return jsonify({
            "code": 404,
            "message": "Supplier not found."
        }), 404

    return jsonify({
        "code": 404,
        "message": "Supplier-ingredient relationship not found."
    }), 404

    

# GET the price_per_unit for an ingredient
@app.route("/supplier_ingredient/ingredient/<int:ingredient_id>/price", methods=['GET'])
def get_price_by_ingredient(ingredient_id):
    supplier_ingredient = db.session.scalar(
        db.select(SupplierIngredient).filter_by(ingredient_id=ingredient_id)
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
@app.route("/supplier_ingredient/ingredient/<int:ingredient_id>/lead_time", methods=['GET'])
def get_lead_time_by_ingredient(ingredient_id):
    supplier_ingredient = db.session.scalar(
        db.select(SupplierIngredient).filter_by(ingredient_id=ingredient_id)
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

    # Check for missing values
    if not data.get("supplier_id") or not data.get("ingredient_id"):
        return jsonify({
            "code": 400,
            "message": "Supplier ID and Ingredient ID are required."
        }), 400
    
    # Check if supplier exists
    supplier = db.session.scalar(
        db.select(Supplier).filter_by(supplier_id=data.get("supplier_id"))
    )
    if not supplier:
        return jsonify({
            "code": 404,
            "message": "Supplier does not exist."
        }), 404
    
    # Check if ingredient already has a supplier
    existing_ingredient = db.session.scalar(
        db.select(SupplierIngredient).filter_by(
            ingredient_id=data.get("ingredient_id")
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

# DELETE a supplier-ingredient relationship
@app.route("/supplier_ingredient/<int:ingredient_id>", methods=['DELETE'])
def delete_supplier_ingredient(ingredient_id):
    
    supplier_ingredient = db.session.scalar(
        db.select(SupplierIngredient).filter_by(ingredient_id=ingredient_id)
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
    app.run(host='0.0.0.0', port=8000, debug=True)