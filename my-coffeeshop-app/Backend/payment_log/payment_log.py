from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ

app = Flask(__name__)
CORS(app)

# Configure Database (MySQL Example)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/payment_log_db'
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Payment Log Model
class PaymentLog(db.Model):
    __tablename__ = 'payment_log'

    payment_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(50), nullable=False)
    outlet_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    # currency = db.Column(db.String(15), nullable=False)
    # payment_method = db.Column(db.String(20), nullable=False)
    payment_id = db.Column(db.String(50), unique=True, nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create Database Tables
with app.app_context():
    db.create_all()

@app.route('/log_payment', methods=['POST'])
def log_payment():
    data = request.json
    try:
        new_log = PaymentLog(
            user_id=data['user_id'],
            outlet_id=data['outlet_id'],
            order_id=data['order_id'],
            amount=data['amount'],
            # payment_method=data['payment_method'],
            payment_id=data['payment_id'],
            payment_status=data['payment_status']
        )
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Payment logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/payment_status/<int:order_id>', methods=['GET'])
def get_payment_status(order_id):
    log = PaymentLog.query.filter_by(order_id=order_id).first()
    if log:
        return jsonify({
            "order_id": log.order_id,
            "payment_status": log.payment_status,
            "amount": log.amount
        })
    return jsonify({"message": "Payment not found"}), 404

@app.route("/payment_log")
def get_all():
    paymentlog = db.session.scalars(db.select(PaymentLog)).all()

    if len(paymentlog):
        return jsonify(
            {
                "code": 200,
                "data": {
                    "payment": [{
                        "user_id": p.user_id,
                        "outlet_id": p.outlet_id,
                        "order_id": p.order_id,
                        "amount": p.amount,
                        "payment_id": p.payment_id,
                        "payment_status": p.payment_status,
                        "created_at": p.created_at.isoformat()
                    } for p in paymentlog]
                }
            }
        )
    return jsonify(
        {
            "code": 404,
            "message": "There are no payments."
        }
    ), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123, debug=True)
