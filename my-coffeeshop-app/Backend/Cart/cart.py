from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import select
from os import environ
from sqlalchemy.orm import clear_mappers



app = Flask(__name__)
CORS(app)

clear_mappers()
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/cart'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}


db = SQLAlchemy(app)

class Cart(db.Model):
    __tablename__ = 'cart'


    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(45), nullable=False)
    outlet_id = db.Column(db.Integer, nullable=False)
    totalPrice = db.Column(db.Float(precision=2), nullable=False)


    def __init__(self, user_id, outlet_id, totalPrice):
        self.user_id = user_id
        self.outlet_id = outlet_id
        self.totalPrice = totalPrice


    def json(self):
        return {"cart_id": self.cart_id, "user_id": self.user_id, "outlet_id": self.outlet_id, "totalPrice": self.totalPrice}



@app.route("/cart")
def get_all():
    cartList = db.session.scalars(db.select(Cart)).all()


    if len(cartList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "carts": [cart.json() for cart in cartList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no carts."
        }
    ), 404



@app.route("/cart/<int:cart_id>")
def filter_byCartID(cart_id):
    cart = db.session.scalar(
    	db.select(Cart).filter_by(cart_id=cart_id)
)


    if cart:
        return jsonify(
            {
                "code": 200,
                "data": cart.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Cart not found."
        }
    ), 404

@app.route("/cart/<string:user_id>/<int:outlet_id>")
def get_byUser(user_id, outlet_id):
    
    # Base query
    query = db.select(Cart)

    # Apply filters if query parameters are provided
    if user_id:
        query = query.where(Cart.user_id == user_id)
    if outlet_id:
        query = query.where(Cart.outlet_id == outlet_id)

    # Execute the query
    cartList = db.session.scalars(query).all()

    # Check if any carts were found
    if len(cartList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "carts": [cart.json() for cart in cartList]
                }
            }
        )
    
    # Return 404 if no carts were found
    return jsonify(
        {
            "code": 404,
            "message": "There are no carts."
        }
    ), 404




@app.route("/cart", methods=['POST'])
def create_cart():
    data = request.get_json()

    # Create a new Cart instance
    cart = Cart(**data)

    try:
        db.session.add(cart)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the cart.",
                "error": str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": cart.json()
        }
    ), 201

@app.route("/cart/<int:cart_id>", methods=['PUT'])
def update_order(cart_id):
    try:
        cart = db.session.scalar(db.select(Cart).filter_by(cart_id=cart_id))
        if not cart:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "cart_id": cart_id
                    },
                    "message": "Cart not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['totalPrice']:
            cart.totalPrice = data['totalPrice']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": cart.json()
                }
            ), 200
    except Exception as e:
        print("Error: {}".format(str(e)))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "cart_id": cart_id
                },
                "message": "An error occurred while updating the cart. " + str(e)
            }
        ), 500
    

@app.route("/cart/<int:cart_id>", methods=["DELETE"])
def delete_by_cartId(cart_id):
    # Find the cart by cartId
    cart = db.session.scalar(
        db.select(Cart).filter_by(cart_id=cart_id)
    )

    if cart:
        # If the cart exists, delete it
        db.session.delete(cart)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Cart deleted successfully."
            }
        )
    else:
        # If the cart does not exist, return a 404 error
        return jsonify(
            {
                "code": 404,
                "message": "Cart not found."
            }
        ), 404   


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5015, debug=True)