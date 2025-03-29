import os
import firebase_admin
from firebase_admin import credentials, auth, firestore
from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from datetime import timedelta
import secrets

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend interaction
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)

# SQL Profile Model
class Profile(db.Model):
    __tablename__ = 'profile'

    userId = db.Column(db.String(45), primary_key=True)
    userName = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    phoneNum = db.Column(db.String(15), nullable=True)

    def json(self):
        return {
            "userId": self.userId,
            "userName": self.userName,
            "email": self.email,
            "phoneNum": self.phoneNum
        }

# Initialize Bcrypt
bcrypt = Bcrypt(app)

# Initialize Firebase Admin SDK
cred = credentials.Certificate('./esd-coffeehouse-firebase-adminsdk-fbsvc-8fcd8a05cd.json')
firebase_admin.initialize_app(cred)

# Firestore client
fs_db = firestore.client()

# ===================== GET PROFILE =====================

@app.route('/profile', methods=['GET'])
def get_profile():
    try:
        id_token = request.headers.get('Authorization')
        print("ID Token:", id_token)

        if not id_token:
            return jsonify({"error": "No token provided"}), 401

        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        print("Decoded UID:", uid)

        profile = db.session.scalar(select(Profile).filter_by(userId=uid))
        print("SQL Profile:", profile)

        if not profile:
            return jsonify({"error": "User profile not found in SQL"}), 404

        return jsonify(profile.json()), 200

    except auth.InvalidIdTokenError:
        print("Invalid Firebase Token")
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        print("Unexpected error:", str(e))  # <-- THIS LINE IS CRITICAL
        return jsonify({"error": "Profile retrieval failed", "details": str(e)}), 500


# ===================== REGISTRATION =====================
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data or 'username' not in data:
            return jsonify({"error": "Missing required fields"}), 400

        user = auth.create_user(
            email=data['email'],
            password=data['password'],
            display_name=data['username']
        )

        # Create Firestore user record
        fs_db.collection('users').document(user.uid).set({
            'username': data['username'],
            'email': data['email'],
            'created_at': firestore.SERVER_TIMESTAMP,
            'role': 'customer'
        })

        # Create SQL profile record
        profile = Profile(userId=user.uid, userName=data['username'], email=data['email'], phoneNum=data.get('phoneNum', ''))
        db.session.add(profile)
        db.session.commit()

        return jsonify({
            "message": "User registered successfully",
            "user_id": user.uid
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Registration failed", "details": str(e)}), 400

# ===================== LOGIN =====================
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({"error": "Missing email"}), 400

        user = auth.get_user_by_email(data['email'])

        profile = db.session.scalar(select(Profile).filter_by(userId=user.uid))
        if not profile:
            return jsonify({"error": "Profile not found in SQL"}), 404

        return jsonify({
            "message": "Login successful",
            "user": profile.json()
        }), 200

    except Exception as e:
        return jsonify({"error": "Login failed", "details": str(e)}), 401

# ===================== PASSWORD RESET =====================
@app.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({"error": "Email is required"}), 400

        reset_link = auth.generate_password_reset_link(data['email'])

        return jsonify({
            "message": "Password reset link generated",
            "reset_link": reset_link
        }), 200

    except Exception as e:
        return jsonify({"error": "Password reset failed", "details": str(e)}), 400


# ===================== LOGOUT =====================
@app.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logout handled by client-side token removal"}), 200

# ===================== ERROR HANDLERS =====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5019, debug=True)