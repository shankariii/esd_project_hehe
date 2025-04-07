from flask import Flask, request
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

app = Flask(__name__)

@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.json
    print(data)
    
    # Hardcoded values
    to_number = "+6590129471"  # Your hardcoded recipient number
    base_message = "Hey Brewer! Your order is ready!"  # Base message
    
    # Get cart ID from request
    cart_id = data.get('cart_id')
    
    # Add cart ID to message if provided
    if cart_id:
        message_body = f"{base_message} Your Cart ID: {cart_id}"
    else:
        message_body = base_message
    
    client = Client(os.getenv('ACCOUNT_SID'), os.getenv('AUTH_TOKEN'))
    message = client.messages.create(
        to=to_number,
        from_="+13149485147",
        body=message_body
    )
    return {"status": "success", "sid": message.sid, "cart_id": cart_id}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)