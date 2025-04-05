from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
# from invokes import invoke_http

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5500, debug=True)