from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe
import pika
import json
import os
from os import environ
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# Configuration
stripe.api_key = environ.get('STRIPE_KEY') or 'rk_test_51QwwPAQRYfaBjPIX2SKCUHNnwPZ2J7ZqRWyEwARvKdQS8IC8kTBFqFBhNUptjTou5qEODE1lr2DwS5kyog06ZyMO004fgzMxEL'
order_service_url = environ.get('ORDER_URL') or 'http://localhost:5001/order'
payment_log_queue = environ.get('PAYMENT_LOG_QUEUE') or 'payment_logs'

# RabbitMQ setup
rabbit_host = environ.get('RABBIT_HOST') or 'localhost'
rabbit_port = environ.get('RABBIT_PORT') or 5672
exchange_name = environ.get('EXCHANGE_NAME') or 'payment_events'
exchange_type = environ.get('EXCHANGE_TYPE') or 'topic'

# Initialize RabbitMQ connection
connection = None
channel = None

def connect_to_rabbitmq():
    global connection, channel
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=rabbit_host, port=rabbit_port))
        channel = connection.channel()
        channel.exchange_declare(
            exchange=exchange_name,
            exchange_type=exchange_type,
            durable=True
        )
        channel.queue_declare(queue=payment_log_queue, durable=True)
        channel.queue_bind(
            exchange=exchange_name,
            queue=payment_log_queue,
            routing_key='payment.*'
        )
    except Exception as e:
        print(f"Failed to connect to RabbitMQ: {str(e)}")
        raise

@app.route('/process-payment', methods=['POST'])
def process_payment():
    if not request.is_json:
        return jsonify({"code": 400, "message": "Invalid JSON input"}), 400

    try:
        data = request.get_json()
        cart_details = data.get('cart_details')
        payment_details = data.get('payment_details')
        
        # 1. Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(float(cart_details['totalPrice']) * 100),  # Convert to cents
            currency='sgd',
            payment_method_types=['card'],
            metadata={
                'user_id': cart_details['user_id'],
                'outlet_id': cart_details['outlet_id']
            }
        )
        
        # 2. Create Order (using your existing order service)
        order_data = {
            'user_id': cart_details['user_id'],
            'items': cart_details['items'],
            'total_amount': cart_details['totalPrice'],
            'payment_intent_id': payment_intent.id
        }
        order_result = invoke_http(order_service_url, method='POST', json=order_data)
        
        if order_result['code'] not in range(200, 300):
            raise Exception(f"Order creation failed: {order_result['message']}")
        
        # 3. Publish payment log to RabbitMQ
        payment_log = {
            'payment_intent_id': payment_intent.id,
            'amount': cart_details['totalPrice'],
            'currency': 'sgd',
            'status': 'succeeded',
            'user_id': cart_details['user_id'],
            'order_id': order_result['data']['order_id'],
            'timestamp': order_result['data']['created']
        }
        
        if not connection or not connection.is_open:
            connect_to_rabbitmq()
            
        channel.basic_publish(
            exchange=exchange_name,
            routing_key='payment.success',
            body=json.dumps(payment_log),
            properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent
            )
        )
        
        # 4. Return success response
        return jsonify({
            'code': 200,
            'data': {
                'client_secret': payment_intent.client_secret,
                'order_id': order_result['data']['order_id'],
                'payment_status': 'succeeded'
            }
        }), 200
        
    except stripe.error.StripeError as e:
        # Handle Stripe-specific errors
        log_payment_error(str(e), data)
        return jsonify({
            'code': 400,
            'message': f'Payment processing failed: {str(e)}'
        }), 400
        
    except Exception as e:
        # Handle other errors
        log_payment_error(str(e), data)
        return jsonify({
            'code': 500,
            'message': f'Internal server error: {str(e)}'
        }), 500

def log_payment_error(error_message, original_data):
    """Log payment errors to RabbitMQ"""
    try:
        if not connection or not connection.is_open:
            connect_to_rabbitmq()
            
        error_log = {
            'error': error_message,
            'original_data': original_data,
            'status': 'failed',
            'timestamp': dastetime.datetime.utcnow().isoformat()
        }
        
        channel.basic_publish(
            exchange=exchange_name,
            routing_key='payment.error',
            body=json.dumps(error_log),
            properties=pika.BasicProperties(
                delivery_mode=2  # Make message persistent
            )
        )
    except Exception as e:
        print(f"Failed to log payment error: {str(e)}")

if __name__ == '__main__':
    print("Starting Payment Composite Service...")
    connect_to_rabbitmq()
    app.run(host='0.0.0.0', port=5200, debug=True)