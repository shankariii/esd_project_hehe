from flask import Flask, jsonify, request
from flask_cors import CORS
import stripe
import json
import os

app = Flask(__name__)
CORS(app)

# Set your secret key. Remember to switch to your live secret key in production!
stripe.api_key = 'rk_test_51QwwPAQRYfaBjPIX2SKCUHNnwPZ2J7ZqRWyEwARvKdQS8IC8kTBFqFBhNUptjTou5qEODE1lr2DwS5kyog06ZyMO004fgzMxEL'  # Replace with your Stripe secret key

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        # Parse the request data
        data = request.get_json()
        print(data)
        amount = int(float(data['amount']))  # Dynamic amount from the frontend
        userid = data['user_id']
        outelt_id = data['outlet_id']
        orderid = data['order_id']
        currency = data.get('currency', 'sgd')  # Default to 'sgd' if not provided

        # Create a PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            automatic_payment_methods={
                    'enabled': True,
                },
            metadata = {
                "User_ID": userid,
                "Outlet_ID": outelt_id,
                "Order_ID": orderid
            }
            # payment_method_types=['card','paynow'],
            # Add additional parameters if needed, such as metadata, description, etc.
        )

        # Return the client secret to the frontend
        return jsonify({
            'client_secret': intent.client_secret,
            # 'intent': intent,
            # 'status': intent.status
        }), 200

        # # In the payment intent service
        # return jsonify({
        #     "code": 200,
        #     "data": {
        #         "id": intent.id,  # include the payment intent ID
        #         "client_secret": intent.client_secret
        #     }
        # })


    except Exception as e:
        # Handle errors
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({
            'error': str(e)
        }), 400

@app.route('/webhook', methods=['POST'])
def webhook_received():
    # You can use webhooks to receive information about asynchronous payment events.
    # For more about our webhook events check out https://stripe.com/docs/webhooks.
    webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')
    request_data = json.loads(request.data)

    if webhook_secret:
        # Retrieve the event by verifying the signature using the raw body and secret if webhook signing is configured.
        signature = request.headers.get('stripe-signature')
        try:
            event = stripe.Webhook.construct_event(
                payload=request.data, sig_header=signature, secret=webhook_secret)
            data = event['data']
        except Exception as e:
            return e
        # Get the type of webhook event sent - used to check the status of PaymentIntents.
        event_type = event['type']
    else:
        data = request_data['data']
        event_type = request_data['type']
    data_object = data['object']

    if event_type == 'payment_intent.succeeded':
        print('💰 Payment received!')
        # Fulfill any orders, e-mail receipts, etc
        # To cancel the payment you will need to issue a Refund (https://stripe.com/docs/api/refunds)
    elif event_type == 'payment_intent.payment_failed':
        print('❌ Payment failed.')
    return jsonify({'status': 'success'})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100, debug=True)