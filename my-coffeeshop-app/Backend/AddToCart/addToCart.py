from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# URLs of individual microservices
cart_service_url = "http://host.docker.internal:5015/cart"
cart_items_service_url = "http://host.docker.internal:5016/cart_items"
cic_service_url = "http://host.docker.internal:5017/cic"

# def get_drink_price(drink_id):
#     """Helper function to get drink price from drinks service"""
#     try:
#         # Make HTTP GET request to Drinks Service
#         response = invoke_http(f"{drinks_service_url}/{drink_id}", method="GET")
#         print("Raw Response from Drinks Service:", response)
        
#         # Extract price directly from the response
#         if "price" in response:  # Check if 'price' exists in the response
#             print("price" + str(response["price"]))
#             return float(response["price"])
#         else:
#             print("Price not found in Drinks Service response.")
#             return 0.0
#     except Exception as e:
#         print(f"Error fetching drink price: {e}")
#         return 0.0
    

# def get_customisation_price(customisations_id):
#     """Helper function to get drink price from drinks service"""
#     try:
#         # Make HTTP GET request to Drinks Service
#         response = invoke_http(f"{customisation_service_url}/{customisations_id}", method="GET")
#         print("Raw Response from Customisation Service:", response)
        
#         # Extract price directly from the response
#         if "price_diff" in response:  # Check if 'price' exists in the response
#             print("price_diff" + str(response["price_diff"]))
#             return float(response["price_diff"])
#         else:
#             print("price_diff not found in Customisation Service response.")
#             return 0.0
#     except Exception as e:
#         print(f"Error fetching customisation price: {e}")
#         return 0.0


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if request.is_json:
        try:
            # Parse the incoming JSON request
            data = request.get_json()
            cart_data = data["cart"]
            cart_items_data = data["cart_items"]
            cic_data = data["cart_item_customisation"]

            # Check if cart already exists for this user and outlet
            user_id = cart_data["user_id"]
            outlet_id = cart_data["outlet_id"]
            check_cart_url = f"{cart_service_url}/{user_id}/{outlet_id}"
            existing_cart = invoke_http(check_cart_url, method="GET")
            
            # Calculate total price from drink prices and quantities
            # total_price = 0.0
            # for item in cart_items_data:
            #     drink_price = get_drink_price(item["drink_id"])
            #     total_price += drink_price * item["quantity"]
            #     print("Total Price = "+  str(total_price))

            if existing_cart["code"] == 200 and existing_cart["data"]["carts"]:
                # Cart exists - update it
                cart_id = existing_cart["data"]["carts"][0]["cart_id"]
                current_total = float(existing_cart["data"]["carts"][0]["totalPrice"])
                new_total = cart_data["totalPrice"]
                sub_total = current_total + new_total
                
                # Update cart with new total price
                update_cart_url = f"{cart_service_url}/{cart_id}"
                update_result = invoke_http(update_cart_url, method="PUT", json={"totalPrice": sub_total})
                
                if update_result["code"] not in range(200, 300):
                    return jsonify({
                        "code": update_result["code"],
                        "message": f"Failed to update cart: {update_result['message']}"
                    }), update_result["code"]
            else:
                # Cart doesn't exist - create new one with calculated total price
                # cart_data["totalPrice"] = total_price
                cart_result = invoke_http(cart_service_url, method="POST", json=cart_data)
                if cart_result["code"] not in range(200, 300):
                    return jsonify({
                        "code": cart_result["code"],
                        "message": f"Failed to add cart: {cart_result['message']}"
                    }), cart_result["code"]
                
                cart_id = cart_result["data"]["cart_id"]

            # Process cart items
            for item in cart_items_data:
                # Check if item already exists in cart
                check_item_url = f"{cart_items_service_url}/check/{cart_id}/{item['drink_id']}"
                existing_item = invoke_http(check_item_url, method="GET")
                
                if existing_item["code"] == 200 and existing_item["data"]:
                    # Item exists - update quantity
                    item_id = existing_item["data"]["cart_items_id"]
                    new_quantity = existing_item["data"]["quantity"] + item["quantity"]
                    update_item_url = f"{cart_items_service_url}/{item_id}"
                    item_result = invoke_http(update_item_url, method="PUT", json={"quantity": new_quantity})
                    
                    if item_result["code"] not in range(200, 300):
                        return jsonify({
                            "code": item_result["code"],
                            "message": f"Failed to update cart item: {item_result['message']}"
                        }), item_result["code"]
                    
                    item["cart_item_id"] = item_id
                else:
                    # Item doesn't exist - add new one
                    item["cart_id_fk"] = cart_id
                    item_result = invoke_http(cart_items_service_url, method="POST", json=item)
                    if item_result["code"] not in range(200, 300):
                        return jsonify({
                            "code": item_result["code"],
                            "message": f"Failed to add cart item: {item_result['message']}"
                        }), item_result["code"]
                    
                    item["cart_item_id"] = item_result["data"]["cart_items_id"]

                # Process customizations (assuming customizations might affect price)
                for customisation in cic_data:
                    customisation["cart_item_id_fk"] = item["cart_item_id"]
                    cic_result = invoke_http(cic_service_url, method="POST", json=customisation)
                    if cic_result["code"] not in range(200, 300):
                        return jsonify({
                            "code": cic_result["code"],
                            "message": f"Failed to add customisations: {cic_result['message']}"
                        }), cic_result["code"]

            # Return success response
            return jsonify({
                "code": 201,
                "message": "Successfully updated cart",
                "data": {
                    "cart_id": cart_id,
                    # "total_price": new_total if 'new_total' in locals() else total_price,
                    "items": [item for item in cart_items_data],
                    "customisations": cic_data
                }
            }), 201

        except Exception as e:
            return jsonify({
                "code": 500,
                "message": f"Internal server error: {str(e)}"
            }), 500

    return jsonify({
        "code": 400,
        "message": "Invalid JSON input"
    }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5200, debug=True)