from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error
from dataclasses import dataclass
import os
import logging
from flasgger import Swagger

app = Flask(__name__)
Swagger(app)

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'coffee_inventory_db'),  # Should match MySQL container name
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'coffee_inventory')
}

def get_db_connection():
    """Retrieve a new database connection dynamically to avoid initialization issues."""
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except Error as e:
        logger.error(f"Error getting database connection: {e}")
        return None

@dataclass
class InventoryItem:
    ingredient_id: str
    available_quantity: float
    unit: str

def dict_from_row(cursor, row):
    """Convert a row to a dictionary based on column names, with a safe check."""
    if not row:
        return None
    columns = [col[0] for col in cursor.description or []]
    return dict(zip(columns, row))

@app.route('/inventory', methods=['GET'])
def get_inventory():
    """
    Get all items in the inventory or filter by ingredient_id
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
    """
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    required_fields = ['ingredient_id', 'available_quantity', 'unit']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute(
            'INSERT INTO inventory (ingredient_id, available_quantity, unit) VALUES (%s, %s, %s)',
            (data['ingredient_id'], data['available_quantity'], data['unit'])
        )
        conn.commit()

        return jsonify({'message': 'Item added successfully'}), 201
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
    Update an existing inventory item (requires all fields)
    """
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    required_fields = ['ingredient_id', 'available_quantity', 'unit']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute(
            'UPDATE inventory SET ingredient_id = %s, available_quantity = %s, unit = %s WHERE inventory_id = %s',
            (data['ingredient_id'], data['available_quantity'], data['unit'], inventory_id)
        )
        conn.commit()

        return jsonify({'message': 'Item updated successfully'})
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
    """
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM inventory WHERE inventory_id = %s', (inventory_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'Item not found'}), 404

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
