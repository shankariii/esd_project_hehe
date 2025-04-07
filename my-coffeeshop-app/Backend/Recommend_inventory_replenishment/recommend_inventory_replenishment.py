from flask import Flask, request, jsonify
from flask_cors import CORS

import os, sys

import requests
from invokes import invoke_http

app = Flask(__name__)
CORS(app)

drink_ingredients_URL = "http://drink_ingredients:5006/ingredients" 
#inventory_URL="http://localhost:8000/api/inventory"
inventory_URL = "http://inventory:5000/inventory"
order_log_items_URL = "https://personal-9fpjlj95.outsystemscloud.com/WorkerUI/rest/UpdateInventoryAPI/UpdateInventory"
supplier_ingredient_URL = "http://supplier_ingredient:8201/supplier_ingredient"
threshold_URL = "http://threshold:8100/threshold"
# threshold_URL="http://localhost:8000/api/threshold"

@app.route("/recommend_inventory_replenishment", methods=['POST'])
def place_order(): #receives order_items JSON array
#checks that the request’s format is JSON and data is valid JSON
    if request.is_json:
        try:
            ingredients_info_order = request.get_json()
            print("\nReceived order_items in JSON:", ingredients_info_order)

            # do the actual work
            result = processInventoryReplenishment(ingredients_info_order)
            return jsonify(result), result["code"] #return to user in json format as a json response

        except Exception as e:
            # Unexpected error in code
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            ex_str = str(e) + " at " + str(exc_type) + ": " + fname + ": line " + str(exc_tb.tb_lineno)
            print(ex_str)

            return jsonify({
                "code": 500,
                "message": "recommend_inventory_replenishment.py internal error: " + ex_str
            }), 500


    # if reached here, not a JSON request.
    return jsonify({
        "code": 400,
        "message": "Invalid JSON input: " + str(request.get_data())
    }), 400

# constants
NUM_DAYS_PERIOD = 7
SAFETY_FACTOR = 1.5

def processInventoryReplenishment(ingredients_info_order):

    all_threshold_responses = []
    thresholds = []
    try:
        # Case: Expected list of ingredients
        if isinstance(ingredients_info_order, list):

            for ing_info in ingredients_info_order:
                ing = ing_info.get('ingredient')
                change_in_quantity = ing_info.get('change_in_quantity')
                unit = ing_info.get('unit')

                if not all([ing, change_in_quantity, unit]):
                        print("Warning: Missing ingredient, quantity, or unit in order items data. Skipping this item record.")
                        continue
                
                try:
                    print('\n-----Invoking inventory microservice-----')
                    #send to inventory (ingredient, change_in_quantity, unit)
                    ing_info_result = invoke_http(inventory_URL, method='POST', json=ing_info)
                    print('ing_info_result', ing_info_result)
                    
                    #  Get change in quantities for the ingredient for the past 7 days
                    ing_history = invoke_http(f"{inventory_URL}/ingredient/{ing}/change_in_quantity", method='GET')
                    if ing_history['code'] not in range(200, 300) or not ing_history.get('data'):
                        print(f"Error: Could not retrieve 7-day history for {ing}")
                        continue

                    print(f"Successful retrieval of changes in quantity for {ing}")
                    amt_used_in_week = sum(item['change_in_quantity'] for item in ing_history['data'])
                    average_daily_usage = abs(amt_used_in_week / NUM_DAYS_PERIOD) if NUM_DAYS_PERIOD > 0 else 0

                    print('\n-----Invoking supplier microservice-----')
                    supplier_result = invoke_http(f"{supplier_ingredient_URL}/ingredient/{ing}/lead_time", method='GET')
                    if supplier_result['code'] not in range(200, 300) or 'lead_time' not in supplier_result.get('data', {}):
                        print(f"Error: Could not retrieve lead time for {ing}")
                        continue

                    print(f"Successful retrieval of lead_time for {ing}")
                    lead_time = supplier_result['data']['lead_time']

                    threshold_value = average_daily_usage * lead_time * SAFETY_FACTOR

                    thresholds.append({
                        "ingredient": ing,
                        "threshold": threshold_value
                    })

                except Exception as e:
                    print(f"Error processing ingredient {ing}: {e}")

            print('\n-----Invoking threshold microservice-----')
            for threshold in thresholds:
                ing = threshold.get("ingredient")
                try:
                    threshold_isexists= invoke_http(f"{threshold_URL}/ingredient/{ing}", method="GET")
                    if threshold_isexists['code'] in range(200,300):
                        threshold_id = threshold_isexists['data'].get("threshold_id")
                        print(f"\nThreshold exists for {ing}, updating threshold")
                        latest_threshold= invoke_http(f"{threshold_URL}/{threshold_id}", method="PUT", json=threshold)
                        
                        if latest_threshold['code'] not in range(200,300):
                            print(f"Error: Cannot update threshold for {ing}")
                    else:
                        print(f"\nThreshold does not exists for {ing}, adding threshold")
                        latest_threshold= invoke_http(f"{threshold_URL}", method="POST", json=threshold)

                    all_threshold_responses.append(latest_threshold)

                except Exception as e:
                    print(f"Error interacting with threshold service for {ing}: {e}")

            return {
                "code": 200,
                "message": "Threshold processing completed.",
                "data": {
                    "threshold_responses": all_threshold_responses
                }
            }
    except Exception as e:
        return {
            "code": 500,
            "message": f"Unexpected error in processInventoryReplenishment: {e}"
        }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8101, debug=True)  
