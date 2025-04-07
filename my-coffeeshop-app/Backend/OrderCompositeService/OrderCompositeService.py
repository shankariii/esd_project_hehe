from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

# Base URLs for microservices
ORDER_BASE_URL = "https://personal-9fpjlj95.outsystemscloud.com/WorkerUI/rest/GetOrderAPI"
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
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON string: {json_str}")
        print(f"Error: {str(e)}")
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
        print(f"[ERROR] Failed to fetch outlet details. Status: {response.status_code}, Response: {response.text}")
        return None
    except Exception as e:
        print(f"[ERROR] Error fetching outlet details: {str(e)}")
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
    except Exception as e:
        print(f"[ERROR] Error fetching drink details: {str(e)}")
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
    except Exception as e:
        print(f"[ERROR] Error fetching customization details: {str(e)}")
        return None

@app.route('/get_orders_by_user/<user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    print(f"\n=== STARTING REQUEST FOR USER {user_id} ===")
    
    try:
        # Step 1: Get all orders for this user
        orders_url = f"{ORDER_BASE_URL}/GetOrderByUserID?user_id={user_id}"
        print(f"[1] Fetching orders from: {orders_url}")
        orders_response = requests.get(orders_url)
        
        if orders_response.status_code != 200:
            return jsonify({
                "code": orders_response.status_code,
                "message": "Failed to fetch orders for user"
            }), orders_response.status_code
        
        orders_data = orders_response.json()
        if "response" not in orders_data:
            return jsonify({
                "code": 500,
                "message": "Unexpected response format from orders service"
            }), 500
        
        if not orders_data["response"]:
            return jsonify({
                "code": 404,
                "message": "No orders found for this user"
            }), 404
        
        orders = []
        for order_str in orders_data["response"]:
            order = parse_nested_json(order_str)
            if not order:
                continue

            order_details = order.get("OrderDetails", {})
            order_id = order_details.get("order_id")
            outlet_id = order_details.get("outlet_id")
            
            if not order_id:
                continue
                
            # Get outlet name
            outlet_name = get_outlet_details(outlet_id)
                
            # Get order items
            order_items_url = f"{ORDER_BASE_URL}/GetOrderItemsByOrderID?order_id={order_id}"
            items_response = requests.get(order_items_url)
            
            order_items = []
            if items_response.status_code == 200:
                items_data = items_response.json()
                if "response" in items_data and items_data["response"]:
                    for item_str in items_data["response"]:
                        item = parse_nested_json(item_str)
                        if not item:
                            continue
                        
                        order_item_id = item.get("OrderItems", {}).get("order_item_id") or item.get("order_item_id")
                        drink_id = item.get("OrderItems", {}).get("drinks_id") or item.get("drinks_id")
                        
                        if not order_item_id or not drink_id:
                            continue
                            
                        # Get drink details
                        drink_details = get_drink_details(drink_id)
                        
                        # Get customizations with names
                        customizations = []
                        customizations_url = f"{ORDER_BASE_URL}/GetOrderItemCustomisationByOIID?order_item_id={order_item_id}"
                        customizations_response = requests.get(customizations_url)
                        
                        print("==================")
                        print(customizations_response)
                        
                        if customizations_response.status_code == 200:
                            customizations_data = customizations_response.json()
                            if "response" in customizations_data and customizations_data["response"]:
                                for cust_str in customizations_data["response"]:
                                    cust = parse_nested_json(cust_str)
                                    if cust:
                                        cust_id = cust.get("OrderItemCustomisation", {}).get("customisation_id") or cust.get("customisation_id")
                                        cust_details = get_customization_details(cust_id) if cust_id else None
                                        
                                        customizations.append({
                                            # "customisation_id": cust_id,
                                            "name": cust_details.get("name") if cust_details else None,
                                            "type": cust_details.get("customisation_type") if cust_details else None,
                                            "price_diff": cust_details.get("price_diff") if cust_details else None,
                                            # "order_item_customisation_id": cust.get("OrderItemCustomisation", {}).get("order_item_customisation") or cust.get("order_item_customisation")
                                        })
                        
                        order_items.append({
                            # "order_item_id": order_item_id,
                            # "drink_id": drink_id,
                            "drink_name": drink_details.get("drink_name") if drink_details else None,
                            "drink_price": drink_details.get("price") if drink_details else None,
                            # "drink_image": drink_details.get("image") if drink_details else None,
                            "quantity": item.get("OrderItems", {}).get("quantity") or item.get("quantity"),
                            "customizations": customizations
                        })
            
            orders.append({
                "order_id": order_id,
                # "outlet_id": outlet_id,
                "outlet_name": outlet_name,
                "total_price": order_details.get("total_price"),
                "status": order_details.get("status"),
                "date_created": order_details.get("timestamp"),
                "items": order_items
            })
        
        print(f"Processed {len(orders)} orders for user {user_id}")
        return jsonify({
            "code": 200,
            "data": {
                "user_id": user_id,
                "orders": orders
            }
        }), 200
    
    except Exception as e:
        print(f"\n!!! UNHANDLED EXCEPTION !!!\n{str(e)}")
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500


@app.route('/get_order_details/<user_id>/<order_id>', methods=['GET'])
def get_order_details(user_id, order_id):
    print(f"\n=== STARTING REQUEST FOR ORDER {order_id} BY USER {user_id} ===")
    
    try:
        # Step 1: Get all orders for this user first to verify ownership
        orders_url = f"{ORDER_BASE_URL}/GetOrderByUserID?user_id={user_id}"
        print(f"[1] Verifying user orders from: {orders_url}")
        orders_response = requests.get(orders_url)
        
        print(f"[DEBUG] Orders response status: {orders_response.status_code}")
        print(f"[DEBUG] Orders response content: {orders_response.text[:500]}...")  # Print first 500 chars to avoid huge logs
        
        if orders_response.status_code != 200:
            print(f"[ERROR] Failed to fetch user orders. Status: {orders_response.status_code}")
            return jsonify({
                "code": orders_response.status_code,
                "message": "Failed to fetch orders for user"
            }), orders_response.status_code
        
        orders_data = orders_response.json()
        print(f"[DEBUG] Parsed orders data: {json.dumps(orders_data, indent=2)[:500]}...")
        
        if "response" not in orders_data:
            print("[ERROR] 'response' field missing in orders data")
            return jsonify({
                "code": 500,
                "message": "Unexpected response format from orders service"
            }), 500
        
        # Check if the requested order_id belongs to this user
        order_found = False
        for order_str in orders_data["response"]:
            order = parse_nested_json(order_str)
            if not order:
                print(f"[WARN] Failed to parse order string: {order_str[:100]}...")
                continue
                
            order_details = order.get("OrderDetails", {})
            print(f"[DEBUG] Checking order ID: {order_details.get('order_id')} (looking for {order_id})")
            
            if str(order_details.get("order_id")) == str(order_id):
                order_found = True
                print(f"[DEBUG] Found matching order: {order_details}")
                break
        
        if not order_found:
            print(f"[ERROR] Order {order_id} not found in user's orders")
            return jsonify({
                "code": 404,
                "message": "Order not found or doesn't belong to this user"
            }), 404
        
        # Step 2: Get the specific order details
        order_url = f"{ORDER_BASE_URL}/GetOrderByOrderID?order_id={order_id}"
        print(f"[2] Fetching order details from: {order_url}")
        order_response = requests.get(order_url)
        
        print(f"[DEBUG] Order details response status: {order_response.status_code}")
        print(f"[DEBUG] Order details response content: {order_response.text[:500]}...")
        
        if order_response.status_code != 200:
            print(f"[ERROR] Failed to fetch order details. Status: {order_response.status_code}")
            return jsonify({
                "code": order_response.status_code,
                "message": "Failed to fetch order details"
            }), order_response.status_code
        
        order_data = order_response.json()
        print(f"[DEBUG] Parsed order data: {json.dumps(order_data, indent=2)[:500]}...")
        
        if "response" not in order_data:
            print("[ERROR] 'response' field missing in order data")
            return jsonify({
                "code": 500,
                "message": "Unexpected response format from order service"
            }), 500
            
        if not order_data["response"]:
            print("[ERROR] Empty response array in order data")
            return jsonify({
                "code": 404,
                "message": "Order details not found"
            }), 404
        
        # Parse the order details
        order_str = order_data["response"][0]  # Get first (should be only) order
        print(f"[DEBUG] Raw order string to parse: {order_str[:200]}...")
        
        order = parse_nested_json(order_str)
        if not order:
            print("[ERROR] Failed to parse order details")
            return jsonify({
                "code": 500,
                "message": "Failed to parse order details"
            }), 500
            
        order_details = order.get("OrderDetails", {})
        print(f"[DEBUG] Parsed order details: {json.dumps(order_details, indent=2)}")
        
        outlet_id = order_details.get("outlet_id")
        print(f"[DEBUG] Outlet ID: {outlet_id}")
        
        # Get outlet name
        outlet_name = get_outlet_details(outlet_id)
        print(f"[DEBUG] Outlet name: {outlet_name}")
            
        # Get order items
        order_items_url = f"{ORDER_BASE_URL}/GetOrderItemsByOrderID?order_id={order_id}"
        print(f"[3] Fetching order items from: {order_items_url}")
        items_response = requests.get(order_items_url)
        
        print(f"[DEBUG] Order items response status: {items_response.status_code}")
        print(f"[DEBUG] Order items response content: {items_response.text[:500]}...")
        
        order_items = []
        if items_response.status_code == 200:
            items_data = items_response.json()
            print(f"[DEBUG] Parsed items data: {json.dumps(items_data, indent=2)[:500]}...")
            
            if "response" in items_data and items_data["response"]:
                for item_str in items_data["response"]:
                    item = parse_nested_json(item_str)
                    if not item:
                        print(f"[WARN] Failed to parse item string: {item_str[:100]}...")
                        continue
                    
                    order_item_id = item.get("OrderItems", {}).get("order_item_id") or item.get("order_item_id")
                    drink_id = item.get("OrderItems", {}).get("drinks_id") or item.get("drinks_id")
                    print(f"[DEBUG] Processing item - ID: {order_item_id}, Drink ID: {drink_id}")
                    
                    if not order_item_id or not drink_id:
                        print(f"[WARN] Missing IDs in item: {item}")
                        continue
                        
                    # Get drink details
                    drink_details = get_drink_details(drink_id)
                    print(f"[DEBUG] Drink details: {drink_details}")
                    
                    # Get customizations with names
                    customizations = []
                    customizations_url = f"{ORDER_BASE_URL}/GetOrderItemCustomisationByOIID?order_item_id={order_item_id}"
                    print(f"[4] Fetching customizations from: {customizations_url}")
                    customizations_response = requests.get(customizations_url)
                    
                    print(f"[DEBUG] Customizations response status: {customizations_response.status_code}")
                    print(f"[DEBUG] Customizations response content: {customizations_response.text[:500]}...")
                    
                    if customizations_response.status_code == 200:
                        customizations_data = customizations_response.json()
                        print(f"[DEBUG] Parsed customizations data: {json.dumps(customizations_data, indent=2)[:500]}...")
                        
                        if "response" in customizations_data and customizations_data["response"]:
                            for cust_str in customizations_data["response"]:
                                cust = parse_nested_json(cust_str)
                                if cust:
                                    cust_id = cust.get("OrderItemCustomisation", {}).get("customisation_id") or cust.get("customisation_id")
                                    print(f"[DEBUG] Processing customization ID: {cust_id}")
                                    
                                    cust_details = get_customization_details(cust_id) if cust_id else None
                                    print(f"[DEBUG] Customization details: {cust_details}")
                                    
                                    customizations.append({
                                        "name": cust_details.get("name") if cust_details else None,
                                        "type": cust_details.get("customisation_type") if cust_details else None,
                                        "price_diff": cust_details.get("price_diff") if cust_details else None,
                                    })
                    
                    order_items.append({
                        "drink_name": drink_details.get("drink_name") if drink_details else None,
                        "drink_price": drink_details.get("price") if drink_details else None,
                        "quantity": item.get("OrderItems", {}).get("quantity") or item.get("quantity"),
                        "customizations": customizations
                    })
        
        # Construct the full order response
        order_response = {
            # "order_id": order_id,
            "outlet_name": outlet_name,
            "total_price": order_details.get("total_price"),
            "status": order_details.get("status"),
            "date_created": order_details.get("timestamp"),
            "items": order_items
        }
        
        print(f"[SUCCESS] Order details:\n{json.dumps(order_response, indent=2)}")
        return jsonify({
            "code": 200,
            "data": {
                "user_id": user_id,
                "order": order_response
            }
        }), 200
    
    except Exception as e:
        print(f"\n!!! UNHANDLED EXCEPTION !!!\n{str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500
    
@app.route('/get_outlet_wait_time/<outlet_id>', methods=['GET'])
def get_outlet_wait_time(outlet_id):
    print(f"\n=== CALCULATING WAIT TIME FOR OUTLET {outlet_id} ===")
    
    try:
        # Step 1: Get all orders for this outlet
        orders_url = f"{ORDER_BASE_URL}/GetOrderByOutletID?outlet_id={outlet_id}"
        print(f"[1] Fetching orders from: {orders_url}")
        orders_response = requests.get(orders_url)
        
        if orders_response.status_code != 200:
            print(f"[ERROR] Failed to fetch outlet orders. Status: {orders_response.status_code}")
            return jsonify({
                "code": orders_response.status_code,
                "message": "Failed to fetch orders for outlet"
            }), orders_response.status_code
        
        orders_data = orders_response.json()
        print(f"[DEBUG] Orders data: {json.dumps(orders_data, indent=2)[:500]}...")
        
        if "response" not in orders_data:
            print("[ERROR] 'response' field missing in orders data")
            return jsonify({
                "code": 500,
                "message": "Unexpected response format from orders service"
            }), 500
        
        if not orders_data["response"]:
            print("[INFO] No orders found for this outlet")
            return jsonify({
                "code": 200,
                "data": {
                    "outlet_id": outlet_id,
                    "total_wait_time_minutes": 0,
                    "order_count": 0,
                    "message": "No orders found for this outlet"
                }
            }), 200
        
        total_wait_time = 0
        order_count = 0
        
        # Step 2: Process each order to calculate wait time
        for order_str in orders_data["response"]:
            order = parse_nested_json(order_str)
            if not order:
                print(f"[WARN] Failed to parse order string: {order_str[:100]}...")
                continue
                
            order_details = order.get("OrderDetails", {})
            order_id = order_details.get("order_id")
            
            if not order_id:
                print("[WARN] Order missing order_id")
                continue
                
            print(f"[2] Processing order {order_id}")
            
            # Step 3: Get order items
            order_items_url = f"{ORDER_BASE_URL}/GetOrderItemsByOrderID?order_id={order_id}"
            items_response = requests.get(order_items_url)
            
            if items_response.status_code != 200:
                print(f"[WARN] Failed to fetch items for order {order_id}")
                continue
                
            items_data = items_response.json()
            
            if "response" not in items_data or not items_data["response"]:
                print(f"[WARN] No items found for order {order_id}")
                continue
                
            # Step 4: Process each item to get preparation time
            for item_str in items_data["response"]:
                item = parse_nested_json(item_str)
                if not item:
                    print(f"[WARN] Failed to parse item string: {item_str[:100]}...")
                    continue
                    
                drink_id = item.get("OrderItems", {}).get("drinks_id") or item.get("drinks_id")
                quantity = item.get("OrderItems", {}).get("quantity") or item.get("quantity", 1)
                
                if not drink_id:
                    print("[WARN] Item missing drink_id")
                    continue
                    
                # Step 5: Get drink details including preparation time
                try:
                    drink_response = requests.get(f"{DRINKS_SERVICE_URL}/{drink_id}")
                    if drink_response.status_code == 200:
                        drink_data = drink_response.json()
                        prep_time = drink_data.get("prep_time_min", 0)
                        total_wait_time += prep_time * quantity
                        print(f"[INFO] Added {prep_time} min (x{quantity}) for drink {drink_id}")
                except Exception as e:
                    print(f"[ERROR] Error fetching drink {drink_id}: {str(e)}")
                    continue
                    
            order_count += 1
        
        print(f"[SUCCESS] Calculated wait time: {total_wait_time} minutes for {order_count} orders")
        
        return jsonify({
            "code": 200,
            "data": {
                "outlet_id": outlet_id,
                "total_wait_time_minutes": total_wait_time,
                "order_count": order_count,
                "average_wait_time_per_order": total_wait_time / order_count if order_count > 0 else 0
            }
        }), 200
    
    except Exception as e:
        print(f"\n!!! UNHANDLED EXCEPTION !!!\n{str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500

if __name__ == "__main__":
    print("Starting Order Composite Service...")
    app.run(host="0.0.0.0", port=5201, debug=True)