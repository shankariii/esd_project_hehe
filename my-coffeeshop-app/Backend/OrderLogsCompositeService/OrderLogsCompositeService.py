from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Base URLs for microservices
ORDER_BASE_URL = "https://personal-9fpjlj95.outsystemscloud.com/WorkerUI/rest/GetOrderLogAPI"
OUTLETS_SERVICE_URL = "http://host.docker.internal:5001/outlets"
DRINKS_SERVICE_URL = "http://host.docker.internal:5005/drinks"
CUSTOMIZATIONS_SERVICE_URL = "http://host.docker.internal:5007/customisations"

def parse_nested_json(json_str):
    """Helper function to parse malformed JSON strings"""
    try:
        cleaned = json_str.replace('\\"', '"').replace('\"', '"')
        if cleaned.startswith('"') and cleaned.endswith('"'):
            cleaned = cleaned[1:-1]
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None

def get_outlet_details(outlet_id):
    """Fetch outlet details from the outlets service"""
    try:
        response = requests.get(f"{OUTLETS_SERVICE_URL}/{outlet_id}")
        
        if response.status_code == 200:
            outlet_data = response.json()
            return {
                "name": outlet_data.get("name"),
                "address": outlet_data.get("address"),
                "position": {
                    "lat": outlet_data.get("position", {}).get("lat"),
                    "lng": outlet_data.get("position", {}).get("lng")
                },
                "queue_count": outlet_data.get("queueCount", 0)
            }
        return None
    except Exception:
        return None

def get_drink_details(drink_id):
    """Fetch drink details from the drinks service"""
    try:
        response = requests.get(f"{DRINKS_SERVICE_URL}/{drink_id}")
        
        if response.status_code == 200:
            drink_data = response.json()
            return {
                "drink_name": drink_data.get("drink_name"),
                "price": drink_data.get("price"),
                "image": drink_data.get("image")
            }
        return None
    except Exception:
        return None

def get_customization_details(customisation_id):
    """Fetch customization details from the customizations service"""
    try:
        response = requests.get(f"{CUSTOMIZATIONS_SERVICE_URL}/{customisation_id}")
        
        if response.status_code == 200:
            cust_data = response.json()
            return {
                "name": cust_data.get("name"),
                "customisation_type": cust_data.get("customisation_type"),
                "price_diff": cust_data.get("price_diff")
            }
        return None
    except Exception:
        return None

@app.route('/get_order_logs_by_user/<user_id>', methods=['GET'])
def get_order_logs_by_user(user_id):
    try:
        # Step 1: Get all order_logs for this user
        order_logs_url = f"{ORDER_BASE_URL}/GetOrderLogByUserID?user_id={user_id}"
        order_logs_response = requests.get(order_logs_url)
        
        if order_logs_response.status_code != 200:
            return jsonify({
                "code": order_logs_response.status_code,
                "message": "Failed to fetch order_logs for user"
            }), order_logs_response.status_code
        
        order_logs_data = order_logs_response.json()
        
        if "response" not in order_logs_data:
            return jsonify({
                "code": 500,
                "message": "Unexpected response format from order_logs service"
            }), 500
        
        if not order_logs_data["response"]:
            return jsonify({
                "code": 404,
                "message": "No order_logs found for this user"
            }), 404
        
        order_logs = []
        for order_str in order_logs_data["response"]:
            order = parse_nested_json(order_str)
            
            if not order:
                continue

            order_details = order.get("OrderLogDetails", {})
            order_id = order_details.get("order_id")
            outlet_id = order_details.get("outlet_id")
            
            if not order_id:
                continue
                
            # Get outlet name
            outlet_details = get_outlet_details(outlet_id)
                
            # Get order items
            order_items_url = f"{ORDER_BASE_URL}/GetOrderLogItemsByOrderID?order_id={order_id}"
            items_response = requests.get(order_items_url)
            
            order_items = []
            if items_response.status_code == 200:
                items_data = items_response.json()
                
                if "response" in items_data and items_data["response"]:
                    for item_str in items_data["response"]:
                        item = parse_nested_json(item_str)
                        
                        if not item:
                            continue
                        
                        order_item_id = item.get("OrderLogItems", {}).get("order_item_id") or item.get("order_item_id")
                        drink_id = item.get("OrderLogItems", {}).get("drinks_id") or item.get("drinks_id")
                        
                        if not order_item_id or not drink_id:
                            continue
                            
                        # Get drink details
                        drink_details = get_drink_details(drink_id)
                        
                        # Get customizations with names
                        customizations = []
                        customizations_url = f"{ORDER_BASE_URL}/GetOrderLogItemCustByOIID?order_item_id={order_item_id}"
                        customizations_response = requests.get(customizations_url)
                        
                        if customizations_response.status_code == 200:
                            customizations_data = customizations_response.json()
                            
                            if "response" in customizations_data and customizations_data["response"]:
                                for cust_str in customizations_data["response"]:
                                    cust = parse_nested_json(cust_str)
                                    
                                    if cust:
                                        cust_id = cust.get("OrderItemCustomisation", {}).get("customisation_id") or cust.get("customisation_id")
                                        cust_details = get_customization_details(cust_id) if cust_id else None
                                        
                                        customizations.append({
                                            "name": cust_details.get("name") if cust_details else None,
                                            "type": cust_details.get("customisation_type") if cust_details else None,
                                            "price_diff": cust_details.get("price_diff") if cust_details else None,
                                        })
                        
                        order_item = {
                            "drink_name": drink_details.get("drink_name") if drink_details else None,
                            "drink_price": drink_details.get("price") if drink_details else None,
                            "quantity": item["OrderLogItems"]["quantity"],
                            "customizations": customizations
                        }
                        order_items.append(order_item)
            
            final_order = {
                "order_id": order_id,
                "outlet_name": outlet_details,
                "total_price": order_details.get("total_price"),
                "status": order_details.get("status"),
                "date_created": order_details.get("timestamp"),
                "items": order_items
            }
            order_logs.append(final_order)
        
        return jsonify({
            "code": 200,
            "data": {
                "user_id": user_id,
                "order_logs": order_logs
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)