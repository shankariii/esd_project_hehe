import pika
import json
from payment_log import db, PaymentLog, app

def consume_logs():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='payment_logs')

    def callback(ch, method, properties, body):
        try:
            log_data = json.loads(body)

            # Check that required fields are in the log_data
            if not all(key in log_data for key in ['user_id', 'order_id', 'amount', 'currency', 'payment_method', 'transaction_id', 'payment_status']):
                print(f"Missing fields in log data: {log_data}")
                return  # Skip invalid log data
            
            with app.app_context():
                # Create a new PaymentLog entry
                new_log = PaymentLog(
                    user_id=log_data['user_id'],
                    order_id=log_data['order_id'],
                    amount=log_data['amount'],
                    currency=log_data['currency'],
                    payment_method=log_data['payment_method'],
                    transaction_id=log_data['transaction_id'],
                    payment_status=log_data['payment_status']  # Make sure it's 'payment_status' in the model
                )
                # Add to the session and commit the transaction
                db.session.add(new_log)
                db.session.commit()
                print(f"Logged Payment: {log_data}")
        except Exception as e:
            print(f"Error processing log data: {e}")

    # Start consuming messages from RabbitMQ
    channel.basic_consume(queue='payment_logs', on_message_callback=callback, auto_ack=True)
    print(" [*] Waiting for payment log messages.")
    channel.start_consuming()

if __name__ == "__main__":
    consume_logs()
