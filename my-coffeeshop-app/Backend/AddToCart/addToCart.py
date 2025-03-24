from flask import Flask, request, jsonify
from flask_cors import CORS
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# URLs of individual microservices
cart_service_url = "http://cart:5015/cart"
cart_items_service_url = "http://cart_items:5016/cart_items"
cic_service_url = "http://cart_items_customisation:5017/cic"


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    if request.is_json:
        try:
            # Parse the incoming JSON request
            data = request.get_json()
            cart_data = data["cart"]
            cart_items_data = data["cart_items"]
            cic_data = data["cart_item_customisation"]

            # Step 1: Add Cart
            cart_result = invoke_http(cart_service_url, method="POST", json=cart_data)
            if cart_result["code"] not in range(200, 300):
                return jsonify({
                    "code": cart_result["code"],
                    "message": f"Failed to add cart: {cart_result['message']}"
                }), cart_result["code"]

            # Retrieve the auto-generated cart_id from the response
            cart_id = cart_result["data"]["cart_id"]

            # Step 2: Add Cart Items
            for item in cart_items_data:
                item["cart_id_fk"] = cart_id  # Associate with the created cart ID
                cart_items_result = invoke_http(cart_items_service_url, method="POST", json=item)
                if cart_items_result["code"] not in range(200, 300):
                    return jsonify({
                        "code": cart_items_result["code"],
                        "message": f"Failed to add cart items: {cart_items_result['message']}"
                    }), cart_items_result["code"]

                # Retrieve the auto-generated cart_item_id from the response
                item["cart_item_id"] = cart_items_result["data"]["cart_items_id"]
                # print(item["cart_item_id"])
                # cart_itemid = cart_items_result["data"]["cart_items_id"]

                # Step 3: Add Customisations for Cart Items
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
                "message": "Successfully added items to cart",
                "data": {
                    "cart": cart_result["data"],
                    "cart_items": [item for item in cart_items_data],
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
