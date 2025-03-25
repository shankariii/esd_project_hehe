from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from flask_cors import CORS
from os import environ



app = Flask(__name__)
CORS(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/profile'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}


db = SQLAlchemy(app)

class Profile(db.Model):
    __tablename__ = 'profile'


    userId = db.Column(db.String(45), primary_key=True)
    userName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phoneNum = db.Column(db.String(15), nullable=False)


    def __init__(self, userId, userName, email, phoneNum):
        self.userId = userId
        self.userName = userName
        self.email = email
        self.phoneNum = phoneNum


    def json(self):
        return {"userId": self.userId, "userName": self.userName, "email": self.email, "phoneNum": self.phoneNum}



@app.route("/profile")
def get_all():
    profileList = db.session.scalars(db.select(Profile)).all()


    if len(profileList):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "carts": [profile.json() for profile in profileList]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no profiles."
        }
    ), 404



@app.route("/profile/<string:userId>")
def find_by_userId(userId):
    profileList = db.session.scalar(
    	db.select(Profile).filter_by(userId=userId)
)


    if profileList:
        return jsonify(
            {
                "code": 200,
                "data": profileList.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "Profile not found."
        }
    ), 404


@app.route("/create_profile", methods=['POST'])
def create_profile():
    data = request.get_json()

    # Create a new Cart instance
    profileList = Profile(**data)

    try:
        db.session.add(profileList)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred creating the Profile.",
                "error": str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": profileList.json()
        }
    ), 201

@app.route("/update_profile/<string:userId>", methods=['PUT'])
def update_profile(userId):
    try:
        # Fetch the profile to be updated
        profile = db.session.scalar(db.select(Profile).filter_by(userId=userId))
        if not profile:
            return jsonify(
                {
                    "code": 404,
                    "data": {
                        "userId": userId
                    },
                    "message": "Profile not found."
                }
            ), 404

        # Get the JSON data from the request
        data = request.get_json()

        # Update fields if they are present in the request
        if 'email' in data:
            profile.email = data['email']
        if 'phoneNum' in data:
            profile.phoneNum = data['phoneNum']
        if 'userName' in data:
            profile.userName = data['userName']

        # Commit changes to the database
        db.session.commit()

        # Return the updated profile
        return jsonify(
            {
                "code": 200,
                "data": profile.json()
            }
        ), 200
    except Exception as e:
        print("Error: {}".format(str(e)))
        return jsonify(
            {
                "code": 500,
                "data": {
                    "userId": userId
                },
                "message": "An error occurred while updating the profile. " + str(e)
            }
        ), 500

@app.route("/delete_profile/<string:userId>", methods=["DELETE"])
def delete_profile(userId):
    # Find the cart by cartId
    profileList = db.session.scalar(
        db.select(Profile).filter_by(userId=userId)
    )

    if profileList:
        # If the cart exists, delete it
        db.session.delete(profileList)
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "message": "Profile deleted successfully."
            }
        )
    else:
        # If the cart does not exist, return a 404 error
        return jsonify(
            {
                "code": 404,
                "message": "Profile not found."
            }
        ), 404   



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5018, debug=True)