from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import pika
import json
from datetime import datetime

app = Flask(__name__)

# Configure Database (MySQL Example)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/payment_log_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define Payment Log Model
class PaymentLog(db.Model):
    __tablename__ = 'payment_log'

    payment_log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    order_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(15), nullable=False)
    payment_method = db.Column(db.String(15), nullable=False)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    payment_status = db.Column(db.String(15), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Create Database Tables
with app.app_context():
    db.create_all()

# HTTP-Based Payment Logging
@app.route('/log_payment', methods=['POST'])
def log_payment():
    data = request.json
    try:
        # Ensure all necessary fields are in the request
        new_log = PaymentLog(
            user_id=data['user_id'],  # User ID must be passed
            order_id=data['order_id'],
            amount=data['amount'],
            currency=data['currency'],
            payment_method=data['payment_method'],
            transaction_id=data['transaction_id'],
            payment_status=data['payment_status']  # Ensure payment_status is passed
        )
        
        db.session.add(new_log)
        db.session.commit()
        return jsonify({"message": "Payment logged successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Retrieve Payment Status
@app.route('/payment_status/<int:order_id>', methods=['GET'])
def get_payment_status(order_id):
    log = PaymentLog.query.filter_by(order_id=order_id).first()
    if log:
        return jsonify({
            "order_id": log.order_id,
            "payment_status": log.payment_status,  # Correct field name for payment status
            "amount": log.amount
        })
    return jsonify({"message": "Payment not found"}), 404

# AMQP: Publish Log Message to RabbitMQ
def publish_to_rabbitmq(order_id, amount, payment_status):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='payment_logs')

        message = json.dumps({
            "order_id": order_id,
            "amount": amount,
            "payment_status": payment_status
        })
        channel.basic_publish(exchange='', routing_key='payment_logs', body=message)

        connection.close()
    except Exception as e:
        print(f"RabbitMQ Error: {e}")

@app.route('/log_payment_async', methods=['POST'])
def log_payment_async():
    data = request.json
    publish_to_rabbitmq(
        data['order_id'], 
        data['amount'], 
        data['payment_status']  # Ensure payment_status is provided
    )
    return jsonify({"message": "Payment log queued for processing"}), 202

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5123, debug=True)