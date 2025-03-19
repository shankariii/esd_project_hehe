from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import pooling, Error
from dataclasses import dataclass
import os
import logging
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print("🔍 DEBUG: MySQL Credentials")
print("Host:", os.environ.get('DB_HOST', 'localhost'))
print("User:", os.environ.get('DB_USER', 'root'))
print("Password:", os.environ.get('DB_PASSWORD'))  # Do NOT log in production, but okay for debugging
print("Database:", os.environ.get('DB_NAME', 'coffee_inventory'))

# Database configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'test',
    #change from test to root later 
    'password': '', 
    'database': 'coffee_inventory'
}

# Database connection pooling
try:
    pool = pooling.MySQLConnectionPool(pool_name="mypool", pool_size=5, **DB_CONFIG)
    logger.info("Database connection pool created successfully")
except Error as e:
    logger.error(f"Error creating database connection pool: {e}")
    pool = None


def get_db_connection():
    """Retrieve a connection from the pool"""
    try:
        if pool:
            return pool.get_connection()
        else:
            logger.error("Database connection pool is not initialized")
            return None
    except Error as e:
        logger.error(f"Error getting connection from pool: {e}")
        return None


@dataclass
class InventoryItem:
    inventory_id: str
    ingredient_id: str
    available_quantity: float
    unit: str


def dict_from_row(cursor, row):
    """Convert a row to a dictionary based on column names"""
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


@app.route('/inventory', methods=['GET'])
def get_inventory():
    """
    Get all items in the inventory or filter by ingredient_id
    ---
    parameters:
      - name: ingredient_id
        in: query
        type: string
        required: false
        description: Filter items by ingredient_id
    responses:
      200:
        description: List of inventory items
    """
    ingredient_id = request.args.get('ingredient_id')

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        query = 'SELECT * FROM inventory' if not ingredient_id else 'SELECT * FROM inventory WHERE ingredient_id = %s'
        params = () if not ingredient_id else (ingredient_id,)

        cursor.execute(query, params)
        rows = cursor.fetchall()
        inventory_items = [dict_from_row(cursor, row) for row in rows]

        return jsonify(inventory_items)
    except Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/inventory/<inventory_id>', methods=['GET'])
def get_item(inventory_id):
    """
    Get a specific item by inventory_id
    ---
    parameters:
      - name: inventory_id
        in: path
        type: string
        required: true
        description: ID of the inventory item
    responses:
      200:
        description: Inventory item details
    """
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM inventory WHERE inventory_id = %s', (inventory_id,))
        row = cursor.fetchone()
        if row is None:
            return jsonify({'error': 'Item not found'}), 404

        return jsonify(dict_from_row(cursor, row))
    except Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/inventory', methods=['POST'])
def add_item():
    """
    Add a new item to the inventory
    ---
    parameters:
      - in: body
        name: body
        schema:
          required:
            - inventory_id
            - ingredient_id
            - available_quantity
            - unit
    responses:
      201:
        description: Item added successfully
    """
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    required_fields = ['inventory_id', 'ingredient_id', 'available_quantity', 'unit']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        item = InventoryItem(**data)
    except ValueError:
        return jsonify({'error': 'Invalid data types'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO inventory (inventory_id, ingredient_id, available_quantity, unit) VALUES (%s, %s, %s, %s)',
            (item.inventory_id, item.ingredient_id, item.available_quantity, item.unit)
        )
        conn.commit()
        return jsonify({'message': 'Item added successfully', 'item': data}), 201
    except Error as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/inventory/<inventory_id>', methods=['PUT'])
def update_item(inventory_id):
    """
    Update an existing inventory item
    ---
    parameters:
      - in: path
        name: inventory_id
        required: true
        type: string
      - in: body
        name: body
    responses:
      200:
        description: Item updated successfully
    """
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    allowed_fields = ['ingredient_id', 'available_quantity', 'unit']
    update_data = {k: v for k, v in data.items() if k in allowed_fields}

    if not update_data:
        return jsonify({'error': 'No valid fields provided'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        set_clause = ', '.join(f"{key} = %s" for key in update_data.keys())
        values = list(update_data.values()) + [inventory_id]

        cursor.execute(f"UPDATE inventory SET {set_clause} WHERE inventory_id = %s", values)
        conn.commit()

        return jsonify({'message': 'Item updated successfully'})
    except Error as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/inventory/<inventory_id>', methods=['PATCH'])
def update_inventory_quantity(inventory_id):
    """
    Update only the available_quantity of an inventory item
    ---
    parameters:
      - in: path
        name: inventory_id
        required: true
        type: string
      - in: body
        name: body
        schema:
          required:
            - available_quantity
    responses:
      200:
        description: Item quantity updated successfully
    """
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()

    if 'available_quantity' not in data:
        return jsonify({'error': 'Missing available_quantity field'}), 400

    try:
        available_quantity = float(data['available_quantity'])
    except ValueError:
        return jsonify({'error': 'Available quantity must be a number'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        # Check if item exists
        cursor.execute('SELECT * FROM inventory WHERE inventory_id = %s', (inventory_id,))
        row = cursor.fetchone()

        if row is None:
            return jsonify({'error': 'Item not found'}), 404

        # Update only available_quantity
        cursor.execute('UPDATE inventory SET available_quantity = %s WHERE inventory_id = %s', 
                      (available_quantity, inventory_id))
        conn.commit()
        return jsonify({'message': f'Item {inventory_id} quantity updated successfully!', 
                       'available_quantity': available_quantity})
    except Error as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/inventory/<inventory_id>', methods=['DELETE'])
def delete_item(inventory_id):
    """
    Delete an inventory item
    ---
    parameters:
      - name: inventory_id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Item deleted successfully
    """
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM inventory WHERE inventory_id = %s', (inventory_id,))
        conn.commit()
        return jsonify({'message': f'Item {inventory_id} deleted successfully'})
    except Error as e:
        conn.rollback()
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error'}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)