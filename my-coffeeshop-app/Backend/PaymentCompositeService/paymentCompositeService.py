from flask import Flask, request, jsonify
from flask_cors import CORS
import os, sys
import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# Define microservice URLs
payment_log_URL = "http://host.docker.internal:5123/log_payment"
order_service_URL = "https://personal-9fpjlj95.outsystemscloud.com/CoffeeShop2/rest/GetCartData/GetCartDetails"
order_items_URL = "https://personal-9fpjlj95.outsystemscloud.com/CoffeeShop2/rest/GetCartData/GetCartItems"
order_customizations_URL = "https://personal-9fpjlj95.outsystemscloud.com/CoffeeShop2/rest/GetCartData/GetCartItemCustomisation"
cart_service_URL = "http://host.docker.internal:5200"

@app.route("/process_payment", methods=['POST'])
def process_payment():
    if request.is_json:
        try:
            payment_data = request.get_json()
            print("\nReceived payment data in JSON:", payment_data)

            result = process_payment_flow(payment_data)
            return jsonify(result), result["code"]

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "process_payment.py internal error: " + ex_str
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

def process_payment_flow(payment_data):
    cart = payment_data.get('cart')
    payment_id = payment_data.get('paymentId')
    payment_status = payment_data.get('paymentStatus')
    
    # 1. Always log the payment regardless of status
    print('\n-----Invoking payment_log microservice-----')
    payment_log_data = {
        "payment_id": payment_id,
        "payment_status": payment_status,
        "order_id": cart.get('cart_id'),
        "outlet_id": cart.get('outlet_id'),
        "user_id": cart.get('user_id'),
        "amount": cart.get('totalPrice')
    }
    
    payment_log_result = invoke_http(
        payment_log_URL, 
        method='POST', 
        json=payment_log_data
    )
    print('payment_log_result:', payment_log_result)
    
    # Check if payment was successful
    if payment_status.lower() != 'succeeded':
        return {
            "code": 200,
            "data": {
                "payment_log_result": payment_log_result
            },
            "message": "Payment not successful - only logged payment"
        }
    
    # 2. Split and process order data
    try:
        # 2a. Create main order record
        print('\n-----Invoking order microservice-----')
        order_data = {
            "cart_id": cart.get('cart_id'),
            "user_id": cart.get('user_id'),
            "outlet_id": cart.get('outlet_id'),
            "totalPrice": cart.get('totalPrice')
            # "payment_id": payment_id
        }
        print(order_data)
        
        order_result = invoke_http(
            order_service_URL,
            method='POST',
            json=order_data
        )
        print('order_result:', order_result)
        order_code = int(order_result.get('code', 500))
        
        # Check if order creation was successful
        if order_code not in range(200, 300):
            print("error order")
            return {
                "code": 400,
                "data": {
                    "payment_log_result": payment_log_result,
                    "order_result": order_result
                },
                "message": "Order creation failed - cart not deleted"
            }
        
        # 2b. Process cart items
        print('\n-----Invoking order items microservice-----')
        items_result = []
        for item in cart.get('items', []):
            item_data = {
                "cart_id_fk": cart.get('cart_id'),
                "cart_items_id": item.get('cart_items_id'),
                "drink_id": item.get('drink_id'),
                "quantity": item.get('quantity')
            }
            
            item_result = invoke_http(
                order_items_URL,
                method='POST',
                json=item_data
            )
            items_result.append(item_result)
            print(f'Item {item.get("drink_id")} result:', item_result)
            
        # 2c. Process customizations for each item
        print('\n-----Invoking order customizations microservice-----')
        customizations_result = []
        for customization in item.get('customisations', []):
            customization_data = {
                "cart_item_id_fk": item.get('cart_items_id'),
                "cic_id": customization.get('cic_id'),
                "customisationId_fk": customization.get('customisationId_fk')
            }
            
            try:
                customization_result = invoke_http(
                    order_customizations_URL,
                    method='POST',
                    json=customization_data
                )
                
                # Ensure we have a proper dictionary response
                if not isinstance(customization_result, dict):
                    customization_result = {"response": str(customization_result)}
                    
                customizations_result.append(customization_result)
                print(f'Customization {customization.get("customisationId_fk")} result:', customization_result)
            
            except Exception as e:
                error_msg = f"Failed to process customization {customization.get('customisationId_fk')}: {str(e)}"
                print(error_msg)
                customizations_result.append({"error": error_msg})
        
        # 3. Delete cart since payment and order creation were successful
        print('\n-----Invoking cart microservice to delete cart-----')
        delete_cart_URL = f"{cart_service_URL}/delete_cart/{cart.get('cart_id')}"
        delete_cart_result = invoke_http(
            delete_cart_URL,
            method='DELETE'
        )
        print('delete_cart_result:', delete_cart_result)
        
        # Return all results
        return {
            "code": 201,
            "data": {
                "payment_log_result": payment_log_result,
                "order_result": order_result,
                "items_result": items_result,
                "customizations_result": customizations_result,
                "delete_cart_result": delete_cart_result
            },
            "message": "Payment processed, order created with items and customizations, and cart deleted successfully"
        }
    
    except Exception as e:
        print(f"Error during order processing: {str(e)}")
        return {
            "code": 500,
            "data": {
                "payment_log_result": payment_log_result
            },
            "message": f"Error during order processing: {str(e)} - cart not deleted"
        }

if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) + " for processing payments...")
    app.run(host="0.0.0.0", port=5300, debug=True)