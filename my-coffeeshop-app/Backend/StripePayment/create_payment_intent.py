from flask import Flask, jsonify, request
from flask_cors import CORS
import stripe

app = Flask(__name__)
CORS(app)

# Set your secret key. Remember to switch to your live secret key in production!
stripe.api_key = 'rk_test_51QwwPAQRYfaBjPIX2SKCUHNnwPZ2J7ZqRWyEwARvKdQS8IC8kTBFqFBhNUptjTou5qEODE1lr2DwS5kyog06ZyMO004fgzMxEL'  # Replace with your Stripe secret key

@app.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    try:
        # Parse the request data
        data = request.get_json()
        amount = int(float(data['amount']))  # Dynamic amount from the frontend
        currency = data.get('currency', 'sgd')  # Default to 'sgd' if not provided

        # Create a PaymentIntent
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency=currency,
            payment_method_types=['card'],
            # Add additional parameters if needed, such as metadata, description, etc.
        )

        # Return the client secret to the frontend
        return jsonify({
            'client_secret': intent.client_secret
        }), 200

    except Exception as e:
        # Handle errors
        print(f"Error: {e}")  # Log the error for debugging
        return jsonify({
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5100, debug=True)