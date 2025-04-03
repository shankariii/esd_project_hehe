from flask import Flask, request
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env variables

app = Flask(__name__)

# @app.route('/send-sms')
# def send_sms():
#     account_sid = os.getenv('ACCOUNT_SID')
#     auth_token = os.getenv('AUTH_TOKEN')
#     client = Client(account_sid, auth_token)

#     message = client.messages.create(
#         to="+6590129471",
#         from_="+13149485147",
#         body="Hello from Dockerized Flask!"
#     )
#     return f"Message SID: {message.sid}"

@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.json
    to_number = data.get('to', '+6590129471')  # Default fallback
    message = data.get('body', 'Hello from Dockerized Flask!')
    
    client = Client(os.getenv('ACCOUNT_SID'), os.getenv('AUTH_TOKEN'))
    message = client.messages.create(
        to=to_number,
        from_="+13149485147",
        body=message
    )
    return {"status": "success", "sid": message.sid}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)