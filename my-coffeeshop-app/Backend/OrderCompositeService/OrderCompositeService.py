from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

# URLs of individual microservices
order_service_url = "https://personal-9fpjlj95.outsystemscloud.com/WorkerUI/rest/GetByOrderID/GetOrder"
order_items_service_url = "https://personal-9fpjlj95.outsystemscloud.com/WorkerUI/rest/GetByOrderID/GetOrderItemCustomisation"
Order_customisation_service_url = "https://personal-9fpjlj95.outsystemscloud.com/WorkerUI/rest/GetByOrderID/GetOrderItems"

@app.route('/orders/count', methods=['GET'])
def get_order_count_by_outlet():
    # Get outlet_id from query parameters
    outlet_id = request.args.get('outlet_id')
    
    if not outlet_id:
        return jsonify({'error': 'outlet_id parameter is required'}), 400
    
    try:
        # Make request to the external API
        response = requests.get(
            order_service_url
        )
        response.raise_for_status()
        
        # Parse the JSON response
        orders_data = response.json()
        
        # Filter orders by outlet_id and count
        try:
            outlet_id_int = int(outlet_id)
            filtered_orders = [
                item['OrderDetails'] for item in orders_data 
                if item.get('OrderDetails', {}).get('outlet_id') == outlet_id_int
            ]
            count = len(filtered_orders)
            
            return jsonify({
                'outlet_id': outlet_id,
                'total_orders': count,
                # 'orders': filtered_orders
            })
        except ValueError:
            return jsonify({'error': 'outlet_id must be an integer'}), 400
        
    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'API request failed: {str(e)}'}), 500
    except json.JSONDecodeError:
        return jsonify({'error': 'Invalid JSON response from API'}), 500
    
@app.route('/get_orders_by_user/<string:user_id>', methods=['GET'])
def get_orders_by_user(user_id):
    try:
        # Step 1: Fetch all orders for this user
        orders_url = f"{order_service_url}/{user_id}"
        orders_response = invoke_http(orders_url, method="GET")
        
        if orders_response["code"] != 200:
            return jsonify({
                "code": orders_response["code"],
                "message": "Failed to fetch orders"
            }), orders_response["code"]
        
        if not orders_response["data"]:
            return jsonify({
                "code": 200,
                "data": [],
                "message": "No orders found for this user"
            }), 200
        
        consolidated_orders = []
        
        # Step 2: For each order, fetch items and customizations
        for order in orders_response["data"]:
            order_id = order["order_id"]
            
            # Fetch order items
            items_url = f"{order_items_service_url}/order/{order_id}"
            items_response = invoke_http(items_url, method="GET")
            
            if items_response["code"] != 200:
                return jsonify({
                    "code": items_response["code"],
                    "message": f"Failed to fetch items for order {order_id}"
                }), items_response["code"]
            
            items_with_customizations = []
            
            # Fetch customizations for each item
            for item in items_response.get("data", []):
                item_id = item["order_item_id"]
                
                customizations_url = f"{Order_customisation_service_url}/item/{item_id}"
                customizations_response = invoke_http(customizations_url, method="GET")
                
                customizations = []
                if customizations_response["code"] == 200:
                    customizations = customizations_response.get("data", [])
                
                # Combine item with its customizations
                item_data = {
                    "order_item_id": item["order_item_id"],
                    "drink_id": item["drink_id"],
                    "quantity": item["quantity"],
                    "price": item["price"],
                    "customizations": customizations
                }
                items_with_customizations.append(item_data)
            
            # Combine order with its items
            consolidated_order = {
                "order_id": order["order_id"],
                "user_id": order["user_id"],
                "outlet_id": order["outlet_id"],
                "order_date": order["order_date"],
                "total_price": order["total_price"],
                "status": order["status"],
                "payment_method": order["payment_method"],
                "items": items_with_customizations
            }
            consolidated_orders.append(consolidated_order)
        
        return jsonify({
            "code": 200,
            "data": consolidated_orders
        }), 200
    
    except Exception as e:
        return jsonify({
            "code": 500,
            "message": f"Internal server error: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)