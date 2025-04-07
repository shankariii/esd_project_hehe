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

def print_debug(title, data):
    """Helper function to print debug information"""
    print(f"\n[DEBUG] {title}")
    print("=" * 50)
    if isinstance(data, (dict, list)):
        print(json.dumps(data, indent=2))
    else:
        print(data)
    print("=" * 50)

def parse_nested_json(json_str):
    """Helper function to parse malformed JSON strings"""
    try:
        print_debug("Original JSON string", json_str)
        cleaned = json_str.replace('\\"', '"').replace('\"', '"')
        if cleaned.startswith('"') and cleaned.endswith('"'):
            cleaned = cleaned[1:-1]
        result = json.loads(cleaned)
        print_debug("Parsed JSON", result)
        return result
    except json.JSONDecodeError as e:
        print(f"[ERROR] Failed to parse JSON string: {json_str}")
        print(f"[ERROR] Error: {str(e)}")
        return None

def get_outlet_details(outlet_id):
    """Fetch outlet details from the outlets service"""
    try:
        print_debug("Fetching outlet details", f"Outlet ID: {outlet_id}")
        response = requests.get(f"{OUTLETS_SERVICE_URL}/{outlet_id}")
        print_debug("Outlet service response", {
            "status_code": response.status_code,
            "content": response.text
        })
        
        if response.status_code == 200:
            outlet_data = response.json()
            result = {
                "name": outlet_data.get("name"),
                "address": outlet_data.get("address"),
                "position": {
                    "lat": outlet_data.get("position", {}).get("lat"),
                    "lng": outlet_data.get("position", {}).get("lng")
                },
                "queue_count": outlet_data.get("queueCount", 0)
            }
            print_debug("Outlet details result", result)
            return result
        
        print(f"[ERROR] Failed to fetch outlet details. Status: {response.status_code}")
        return None
    except Exception as e:
        print(f"[ERROR] Error fetching outlet details: {str(e)}")
        return None

def get_drink_details(drink_id):
    """Fetch drink details from the drinks service"""
    try:
        print_debug("Fetching drink details", f"Drink ID: {drink_id}")
        response = requests.get(f"{DRINKS_SERVICE_URL}/{drink_id}")
        print_debug("Drink service response", {
            "status_code": response.status_code,
            "content": response.text
        })
        
        if response.status_code == 200:
            drink_data = response.json()
            result = {
                "drink_name": drink_data.get("drink_name"),
                "price": drink_data.get("price"),
                "image": drink_data.get("image")
            }
            print_debug("Drink details result", result)
            return result
        
        print(f"[ERROR] Failed to fetch drink details. Status: {response.status_code}")
        return None
    except Exception as e:
        print(f"[ERROR] Error fetching drink details: {str(e)}")
        return None

def get_customization_details(customisation_id):
    """Fetch customization details from the customizations service"""
    try:
        print_debug("Fetching customization details", f"Customization ID: {customisation_id}")
        response = requests.get(f"{CUSTOMIZATIONS_SERVICE_URL}/{customisation_id}")
        print_debug("Customization service response", {
            "status_code": response.status_code,
            "content": response.text
        })
        
        if response.status_code == 200:
            cust_data = response.json()
            result = {
                "name": cust_data.get("name"),
                "customisation_type": cust_data.get("customisation_type"),
                "price_diff": cust_data.get("price_diff")
            }
            print_debug("Customization details result", result)
            return result
        
        print(f"[ERROR] Failed to fetch customization details. Status: {response.status_code}")
        return None
    except Exception as e:
        print(f"[ERROR] Error fetching customization details: {str(e)}")
        return None

@app.route('/get_order_logs_by_user/<user_id>', methods=['GET'])
def get_order_logs_by_user(user_id):
    print(f"\n=== STARTING REQUEST FOR USER {user_id} ===")
    
    try:
        # Step 1: Get all order_logs for this user
        order_logs_url = f"{ORDER_BASE_URL}/GetOrderLogByUserID?user_id={user_id}"
        print(f"[1] Fetching order_logs from: {order_logs_url}")
        order_logs_response = requests.get(order_logs_url)
        
        print_debug("Initial order logs response", {
            "status_code": order_logs_response.status_code,
            "content": order_logs_response.text
        })
        
        if order_logs_response.status_code != 200:
            return jsonify({
                "code": order_logs_response.status_code,
                "message": "Failed to fetch order_logs for user"
            }), order_logs_response.status_code
        
        order_logs_data = order_logs_response.json()
        print_debug("Order logs data", order_logs_data)
        
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
        for idx, order_str in enumerate(order_logs_data["response"]):
            print(f"\nProcessing order {idx + 1}/{len(order_logs_data['response'])}")
            print_debug("Raw order string", order_str)
            
            order = parse_nested_json(order_str)
            print_debug("Parsed order", order)
            
            if not order:
                print("[WARNING] Skipping malformed order")
                continue

            order_details = order.get("OrderLogDetails", {})
            print_debug("Order details", order_details)
            
            order_id = order_details.get("order_id")
            outlet_id = order_details.get("outlet_id")
            
            if not order_id:
                print("[WARNING] Order missing order_id, skipping")
                continue
                
            print(f"Processing order ID: {order_id}, Outlet ID: {outlet_id}")
            
            # Get outlet name
            outlet_details = get_outlet_details(outlet_id)
            print_debug("Outlet details", outlet_details)
                
            # Get order items
            order_items_url = f"{ORDER_BASE_URL}/GetOrderLogItemsByOrderID?order_id={order_id}"
            print(f"Fetching items from: {order_items_url}")
            items_response = requests.get(order_items_url)
            
            print_debug("Items response", {
                "status_code": items_response.status_code,
                "content": items_response.text
            })
            
            order_items = []
            if items_response.status_code == 200:
                items_data = items_response.json()
                print_debug("Items data", items_data)
                
                if "response" in items_data and items_data["response"]:
                    for item_idx, item_str in enumerate(items_data["response"]):
                        print(f"\nProcessing item {item_idx + 1}/{len(items_data['response'])}")
                        print_debug("Raw item string", item_str)
                        
                        item = parse_nested_json(item_str)
                        print_debug("Parsed item", item)
                        
                        if not item:
                            print("[WARNING] Skipping malformed item")
                            continue
                        
                        order_item_id = item.get("OrderLogItems", {}).get("order_item_id") or item.get("order_item_id")
                        drink_id = item.get("OrderLogItems", {}).get("drinks_id") or item.get("drinks_id")
                        
                        if not order_item_id or not drink_id:
                            print(f"[WARNING] Missing IDs in item (order_item_id: {order_item_id}, drink_id: {drink_id})")
                            continue
                            
                        print(f"Processing item ID: {order_item_id}, Drink ID: {drink_id}")
                        
                        # Get drink details
                        drink_details = get_drink_details(drink_id)
                        print_debug("Drink details", drink_details)
                        
                        # Get customizations with names
                        customizations = []
                        customizations_url = f"{ORDER_BASE_URL}/GetOrderLogItemCustByOIID?order_item_id={order_item_id}"
                        print(f"Fetching customizations from: {customizations_url}")
                        customizations_response = requests.get(customizations_url)
                        
                        print_debug("Customizations response", {
                            "status_code": customizations_response.status_code,
                            "content": customizations_response.text
                        })
                        
                        if customizations_response.status_code == 200:
                            customizations_data = customizations_response.json()
                            print_debug("Customizations data", customizations_data)
                            
                            if "response" in customizations_data and customizations_data["response"]:
                                for cust_idx, cust_str in enumerate(customizations_data["response"]):
                                    print(f"\nProcessing customization {cust_idx + 1}/{len(customizations_data['response'])}")
                                    print_debug("Raw customization string", cust_str)
                                    
                                    cust = parse_nested_json(cust_str)
                                    print_debug("Parsed customization", cust)
                                    
                                    if cust:
                                        cust_id = cust.get("OrderItemCustomisation", {}).get("customisation_id") or cust.get("customisation_id")
                                        print(f"Processing customization ID: {cust_id}")
                                        
                                        cust_details = get_customization_details(cust_id) if cust_id else None
                                        print_debug("Customization details", cust_details)
                                        
                                        customizations.append({
                                            "name": cust_details.get("name") if cust_details else None,
                                            "type": cust_details.get("customisation_type") if cust_details else None,
                                            "price_diff": cust_details.get("price_diff") if cust_details else None,
                                        })
                                        print_debug("Current customizations list", customizations)
                        
                        order_item = {
                            "drink_name": drink_details.get("drink_name") if drink_details else None,
                            "drink_price": drink_details.get("price") if drink_details else None,
                            "quantity": item.get("OrderItems", {}).get("quantity") or item.get("quantity"),
                            "customizations": customizations
                        }
                        print_debug("Final order item", order_item)
                        order_items.append(order_item)
            
            final_order = {
                "order_id": order_id,
                "outlet_name": outlet_details,
                "total_price": order_details.get("total_price"),
                "status": order_details.get("status"),
                "date_created": order_details.get("timestamp"),
                "items": order_items
            }
            print_debug("Final order log entry", final_order)
            order_logs.append(final_order)
        
        print(f"\nProcessed {len(order_logs)} order_logs for user {user_id}")
        print_debug("Final response data", {
            "user_id": user_id,
            "order_logs": order_logs
        })
        
        return jsonify({
            "code": 200,
            "data": {
                "user_id": user_id,
                "order_logs": order_logs
            }
        }), 200
    
    except Exception as e:
        print(f"\n!!! UNHANDLED EXCEPTION !!!")
        print_debug("Exception details", {
            "type": type(e).__name__,
            "message": str(e),
            "args": e.args
        })
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500

if __name__ == "__main__":
    print("Starting Order Composite Service...")
    app.run(host="0.0.0.0", port=5500, debug=True)