from flask import Flask, jsonify, request
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

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''), 
    'database': os.environ.get('DB_NAME', 'outlet')
}

# Database connection pooling
try:
    pool = pooling.MySQLConnectionPool(pool_name="outletpool", pool_size=5, **DB_CONFIG)
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
class Outlet:
    outlet_id: int
    name: str
    address: str
    latitude: float
    longitude: float
    contact_info: str


def dict_from_row(cursor, row):
    """Convert a row to a dictionary based on column names"""
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, row))


@app.route('/outlets', methods=['GET'])
def get_all_outlets():
    """
    Get all coffee shop outlets or filter by name
    ---
    parameters:
      - name: name
        in: query
        type: string
        required: false
        description: Filter outlets by name (case-insensitive partial match)
    responses:
      200:
        description: List of coffee shop outlets
      500:
        description: Database connection error
    """
    name_filter = request.args.get('name')

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        if name_filter:
            query = 'SELECT * FROM outlets WHERE name LIKE %s'
            cursor.execute(query, (f'%{name_filter}%',))
        else:
            query = 'SELECT * FROM outlets'
            cursor.execute(query)
            
        rows = cursor.fetchall()
        outlets = [dict_from_row(cursor, row) for row in rows]

        return jsonify(outlets)
    except Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/outlets/<int:outlet_id>', methods=['GET'])
def get_outlet_by_id(outlet_id):
    """
    Get a specific coffee shop outlet by ID
    ---
    parameters:
      - name: outlet_id
        in: path
        type: integer
        required: true
        description: ID of the outlet to retrieve
    responses:
      200:
        description: Outlet details
      404:
        description: Outlet not found
      500:
        description: Database connection error
    """
    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        cursor.execute('SELECT * FROM outlets WHERE outlet_id = %s', (outlet_id,))
        row = cursor.fetchone()
        
        if row is None:
            return jsonify({'error': 'Outlet not found'}), 404

        outlet = dict_from_row(cursor, row)
        return jsonify(outlet)
    except Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


@app.route('/outlets/nearby', methods=['GET'])
def get_nearby_outlets():
    """
    Find outlets near a specific location
    ---
    parameters:
      - name: lat
        in: query
        type: number
        required: true
        description: Latitude of the search point
      - name: lon
        in: query
        type: number
        required: true
        description: Longitude of the search point
      - name: radius
        in: query
        type: number
        required: false
        default: 5.0
        description: Search radius in kilometers
    responses:
      200:
        description: List of nearby outlets with distances
      400:
        description: Missing required parameters
      500:
        description: Database connection error
    """
    try:
        lat = float(request.args.get('lat'))
        lon = float(request.args.get('lon'))
        radius = float(request.args.get('radius', 5.0))
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid parameters. lat, lon must be numbers'}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({'error': 'Database connection failed'}), 500

    cursor = conn.cursor()
    try:
        # Haversine formula to calculate distance between two points on Earth
        # This calculates distances in kilometers
        haversine_formula = """
        SELECT *, 
        (6371 * acos(cos(radians(%s)) * cos(radians(latitude)) * 
        cos(radians(longitude) - radians(%s)) + sin(radians(%s)) * 
        sin(radians(latitude)))) AS distance 
        FROM outlets 
        HAVING distance < %s 
        ORDER BY distance
        """
        cursor.execute(haversine_formula, (lat, lon, lat, radius))
        rows = cursor.fetchall()
        
        # Add distance to the outlet dictionary
        columns = [col[0] for col in cursor.description]
        outlets = []
        for row in rows:
            outlet = dict(zip(columns, row))
            outlets.append(outlet)

        return jsonify(outlets)
    except Error as e:
        logger.error(f"Database error: {e}")
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    finally:
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)