from flask import Flask, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/get_cart_details/<user_id>/<int:outlet_id>', methods=['GET'])
def get_cart_details(user_id, outlet_id):
    try:
        # Step 1: Fetch cart information
        cart_url = f"http://host.docker.internal:5015/cart/{user_id}/{outlet_id}"
        cart_response = requests.get(cart_url)
        
        if cart_response.status_code != 200 or not cart_response.text.strip():
            return jsonify({"code": 500, "message": "Failed to fetch cart information"}), 500
        
        cart_data = cart_response.json()
        if "data" not in cart_data or not cart_data["data"]["carts"]:
            return jsonify({"code": 404, "message": "Cart not found"}), 404
        
        cart = cart_data["data"]["carts"][0]
        cart_id = cart["cart_id"]
        
        # Step 2: Fetch cart items
        cart_items_url = f"http://host.docker.internal:5016/cart_items_cartId/{cart_id}"
        cart_items_response = requests.get(cart_items_url)
        
        if cart_items_response.status_code != 200 or not cart_items_response.text.strip():
            return jsonify({"code": 500, "message": "Failed to fetch cart items"}), 500
        
        cart_items_data = cart_items_response.json()
        if "data" not in cart_items_data or not cart_items_data["data"]:
            return jsonify({"code": 404, "message": "Cart items not found"}), 404
        
        cart_items = []
        
        # Step 3: Fetch customizations and consolidate data
        for item in cart_items_data["data"]:
            cic_url = f"http://host.docker.internal:5017/cic/{item['cart_items_id']}"
            cic_response = requests.get(cic_url)
            
            customisations = None
            if cic_response.status_code == 200 and cic_response.text.strip():
                cic_data = cic_response.json()
                customisations = cic_data.get("data", None)
            
            # Consolidate relevant fields for this item
            consolidated_item = {
                "drink_id": item["drink_id"],
                "quantity": item["quantity"],
                "customisations": customisations
            }
            cart_items.append(consolidated_item)
        
        # Step 4: Final consolidated response
        consolidated_data = {
            "cart_id": cart["cart_id"],
            "user_id": cart["user_id"],
            "outlet_id": cart["outlet_id"],
            "totalPrice": cart["totalPrice"],
            "items": cart_items
        }
        
        return jsonify({"code": 200, "data": consolidated_data}), 200
    
    except Exception as e:
        return jsonify({"code": 500, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5300, debug=True)
