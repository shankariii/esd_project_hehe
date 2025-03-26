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

class Cart_Items_Customisation(db.Model):
    __tablename__ = 'cart_items_customisation'


    cic_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart_item_id_fk = db.Column(db.Integer, nullable=False)
    customisationId_fk = db.Column(db.Integer, nullable=False)


    def __init__(self, cart_item_id_fk, customisationId_fk):
        self.cart_item_id_fk = cart_item_id_fk
        self.customisationId_fk = customisationId_fk


    def json(self):
        return {"cic_id": self.cic_id, "cart_item_id_fk": self.cart_item_id_fk, "customisationId_fk": self.customisationId_fk}


#Get all the items in the Cart_item_customisation table
@app.route("/cic")
def get_all_cic():
    cicList = db.session.scalars(db.select(Cart_Items_Customisation)).all()


    if len(cicList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "cic": [cic.json() for cic in cicList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no CIC items."
        }
    ), 404


#Get items from Cart_items based on the cart_item_id
# @app.route("/cic/<int:cic_id>")
# def find_cic_by_id(cic_id):
#     cicList = db.session.scalar(
#     	db.select(Cart_Items_Customisation).filter_by(cic_id = cic_id)
# )


#     if cicList:
#         return jsonify(
#             {
#                 "code": 200,
#                 "data": cicList.json()
#             }
#         )
#     return jsonify(
#         {
#             "code": 404,
#             "message": "CIC Item not found."
#         }
#     ), 404

@app.route("/cic/<int:cart_item_id_fk>")
def find_cic_by_id(cart_item_id_fk):
#     cicList = db.session.scalar(
#     	db.select(Cart_Items_Customisation).filter_by(cart_item_id_fk = cart_item_id_fk)
# )
    cicList = db.session.scalars(
            select(Cart_Items_Customisation).where(Cart_Items_Customisation.cart_item_id_fk == cart_item_id_fk)
        ).all()


    if cicList:
        return jsonify(
            {
                "code": 200,
                "data": [item.json() for item in cicList]
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "CIC Item not found."
        }
    ), 404

@app.route("/cic", methods=['POST'])
def create_cic():
    data = request.get_json()

    # Create a new Cart instance
    cicList = Cart_Items_Customisation(**data)

    try:
        db.session.add(cicList)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the CIC.",
                "error": str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": cicList.json()
        }
    ), 201

@app.route("/cic/<int:cic_id>", methods=['PUT'])
def update_customisation(cic_id):
    try:
        cicList = db.session.scalar(db.select(Cart_Items_Customisation).filter_by(cic_id=cic_id))
        if not cicList:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "cic_id": cic_id
                    },
                    "message": "CustomisationId not found."
                }
            ), 404

        # update status
        data = request.get_json()
        if data['customisationId_fk']:
            cicList.customisationId_fk = data['customisationId_fk']
            db.session.commit()
            return jsonify(
                {
                    "code": 200,
                    "data": cicList.json()
                }
            ), 200
    except Exception as e:
        print("Error: {}".format(str(e)))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "cic_id": cic_id
                },
                "message": "An error occurred while updating the customisation. " + str(e)
            }
        ), 500
    
@app.route("/cic/<int:cic_id>", methods=["DELETE"])
def delete_by_cicId(cic_id):
    # Find the cart by cartId
    cicList = db.session.scalar(
        db.select(Cart_Items_Customisation).filter_by(cic_id=cic_id)
    )

    if cicList:
        # If the cart exists, delete it
        db.session.delete(cicList)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "CIC Item deleted successfully."
            }
        )
    else:
        # If the cart does not exist, return a 404 error
        return jsonify(
            {
                "code": 404,
                "message": "CIC Item not found."
            }
        ), 404   



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5017, debug=True)