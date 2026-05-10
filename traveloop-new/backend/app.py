"""
Traveloop Flask Backend
Main application file with all API routes
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from functools import wraps
import sqlite3
import hashlib
import secrets
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = secrets.token_hex(32)

DATABASE = 'traveloop.db'

# ============== DATABASE SETUP ==============

def get_db():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database with all tables"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            avatar TEXT DEFAULT '',
            phone TEXT DEFAULT '',
            location TEXT DEFAULT '',
            bio TEXT DEFAULT '',
            preferences TEXT DEFAULT '{}',
            is_admin INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Sessions table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Trips table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS trips (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            description TEXT DEFAULT '',
            start_date DATE,
            end_date DATE,
            cover_image TEXT DEFAULT '',
            budget REAL DEFAULT 0,
            currency TEXT DEFAULT 'USD',
            is_public INTEGER DEFAULT 0,
            share_code TEXT UNIQUE,
            status TEXT DEFAULT 'upcoming',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Stops/Destinations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS stops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            city TEXT NOT NULL,
            country TEXT DEFAULT '',
            start_date DATE,
            end_date DATE,
            order_index INTEGER DEFAULT 0,
            notes TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
        )
    ''')
    
    # Activities table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            stop_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT DEFAULT 'sightseeing',
            description TEXT DEFAULT '',
            location TEXT DEFAULT '',
            date DATE,
            time TEXT DEFAULT '',
            duration TEXT DEFAULT '',
            cost REAL DEFAULT 0,
            is_booked INTEGER DEFAULT 0,
            booking_reference TEXT DEFAULT '',
            order_index INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (stop_id) REFERENCES stops(id) ON DELETE CASCADE
        )
    ''')
    
    # Budget items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS budget_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            description TEXT DEFAULT '',
            amount REAL NOT NULL,
            currency TEXT DEFAULT 'USD',
            is_paid INTEGER DEFAULT 0,
            date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
        )
    ''')
    
    # Packing items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS packing_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            category TEXT DEFAULT 'essentials',
            quantity INTEGER DEFAULT 1,
            is_packed INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE
        )
    ''')
    
    # Notes/Journal table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            stop_id INTEGER,
            title TEXT NOT NULL,
            content TEXT DEFAULT '',
            mood TEXT DEFAULT '',
            images TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
            FOREIGN KEY (stop_id) REFERENCES stops(id) ON DELETE SET NULL
        )
    ''')
    
    # Saved destinations table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_destinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            city TEXT NOT NULL,
            country TEXT DEFAULT '',
            region TEXT DEFAULT '',
            image TEXT DEFAULT '',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    ''')
    
    # Trip collaborators table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS collaborators (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trip_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            role TEXT DEFAULT 'viewer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (trip_id) REFERENCES trips(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE(trip_id, user_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# ============== AUTHENTICATION HELPERS ==============

def hash_password(password):
    """Hash password with salt"""
    salt = secrets.token_hex(16)
    hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
    return f"{salt}${hash_obj.hex()}"

def verify_password(password, password_hash):
    """Verify password against hash"""
    try:
        salt, hash_value = password_hash.split('$')
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return hash_obj.hex() == hash_value
    except:
        return False

def generate_token():
    """Generate a secure session token"""
    return secrets.token_urlsafe(64)

def create_session(user_id):
    """Create a new session for user"""
    conn = get_db()
    cursor = conn.cursor()
    
    token = generate_token()
    expires_at = datetime.now() + timedelta(days=7)
    
    cursor.execute('''
        INSERT INTO sessions (user_id, token, expires_at)
        VALUES (?, ?, ?)
    ''', (user_id, token, expires_at))
    
    conn.commit()
    conn.close()
    return token

def get_user_from_token(token):
    """Get user from session token"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT u.* FROM users u
        JOIN sessions s ON u.id = s.user_id
        WHERE s.token = ? AND s.expires_at > ?
    ''', (token, datetime.now()))
    
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None

def login_required(f):
    """Decorator for protected routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Authentication required'}), 401
        
        user = get_user_from_token(token)
        if not user:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        request.user = user
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator for admin-only routes"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not request.user.get('is_admin'):
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

def dict_from_row(row):
    """Convert sqlite3.Row to dictionary"""
    return dict(row) if row else None

# ============== AUTH ROUTES ==============

@app.route('/api/auth/signup', methods=['POST'])
def signup():
    """Register a new user"""
    data = request.json
    
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return jsonify({'error': 'Name, email and password are required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if user exists
    cursor.execute('SELECT id FROM users WHERE email = ?', (data['email'],))
    if cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create user
    password_hash = hash_password(data['password'])
    cursor.execute('''
        INSERT INTO users (name, email, password_hash)
        VALUES (?, ?, ?)
    ''', (data['name'], data['email'], password_hash))
    
    user_id = cursor.lastrowid
    conn.commit()
    
    # Create session
    token = create_session(user_id)
    
    cursor.execute('SELECT id, name, email, avatar, is_admin FROM users WHERE id = ?', (user_id,))
    user = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({
        'message': 'User created successfully',
        'token': token,
        'user': user
    }), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE email = ?', (data['email'],))
    user = cursor.fetchone()
    
    if not user or not verify_password(data['password'], user['password_hash']):
        conn.close()
        return jsonify({'error': 'Invalid email or password'}), 401
    
    token = create_session(user['id'])
    
    user_dict = dict_from_row(user)
    del user_dict['password_hash']
    conn.close()
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user_dict
    })

@app.route('/api/auth/logout', methods=['POST'])
@login_required
def logout():
    """Logout user"""
    token = request.headers.get('Authorization', '').replace('Bearer ', '')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sessions WHERE token = ?', (token,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/auth/me', methods=['GET'])
@login_required
def get_current_user():
    """Get current logged in user"""
    user = request.user.copy()
    if 'password_hash' in user:
        del user['password_hash']
    return jsonify({'user': user})

# ============== USER ROUTES ==============

@app.route('/api/users/profile', methods=['PUT'])
@login_required
def update_profile():
    """Update user profile"""
    data = request.json
    user_id = request.user['id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    allowed_fields = ['name', 'avatar', 'phone', 'location', 'bio']
    updates = []
    values = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f'{field} = ?')
            values.append(data[field])
    
    if data.get('preferences'):
        updates.append('preferences = ?')
        values.append(json.dumps(data['preferences']))
    
    if updates:
        values.append(user_id)
        cursor.execute(f'''
            UPDATE users SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', values)
        conn.commit()
    
    cursor.execute('SELECT id, name, email, avatar, phone, location, bio, preferences FROM users WHERE id = ?', (user_id,))
    user = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Profile updated', 'user': user})

@app.route('/api/users/password', methods=['PUT'])
@login_required
def change_password():
    """Change user password"""
    data = request.json
    user_id = request.user['id']
    
    if not data.get('current_password') or not data.get('new_password'):
        return jsonify({'error': 'Current and new password required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT password_hash FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    
    if not verify_password(data['current_password'], user['password_hash']):
        conn.close()
        return jsonify({'error': 'Current password is incorrect'}), 400
    
    new_hash = hash_password(data['new_password'])
    cursor.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hash, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Password updated successfully'})

# ============== TRIP ROUTES ==============

@app.route('/api/trips', methods=['GET'])
@login_required
def get_trips():
    """Get all trips for current user"""
    user_id = request.user['id']
    status = request.args.get('status')
    
    conn = get_db()
    cursor = conn.cursor()
    
    query = 'SELECT * FROM trips WHERE user_id = ?'
    params = [user_id]
    
    if status and status != 'all':
        query += ' AND status = ?'
        params.append(status)
    
    query += ' ORDER BY created_at DESC'
    
    cursor.execute(query, params)
    trips = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'trips': trips})

@app.route('/api/trips/<int:trip_id>', methods=['GET'])
@login_required
def get_trip(trip_id):
    """Get single trip with all details"""
    user_id = request.user['id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM trips WHERE id = ? AND user_id = ?', (trip_id, user_id))
    trip = dict_from_row(cursor.fetchone())
    
    if not trip:
        conn.close()
        return jsonify({'error': 'Trip not found'}), 404
    
    # Get stops
    cursor.execute('SELECT * FROM stops WHERE trip_id = ? ORDER BY order_index', (trip_id,))
    stops = [dict_from_row(row) for row in cursor.fetchall()]
    
    # Get activities for each stop
    for stop in stops:
        cursor.execute('SELECT * FROM activities WHERE stop_id = ? ORDER BY order_index', (stop['id'],))
        stop['activities'] = [dict_from_row(row) for row in cursor.fetchall()]
    
    trip['stops'] = stops
    
    # Get budget items
    cursor.execute('SELECT * FROM budget_items WHERE trip_id = ?', (trip_id,))
    trip['budget_items'] = [dict_from_row(row) for row in cursor.fetchall()]
    
    # Get packing items
    cursor.execute('SELECT * FROM packing_items WHERE trip_id = ?', (trip_id,))
    trip['packing_items'] = [dict_from_row(row) for row in cursor.fetchall()]
    
    # Get notes
    cursor.execute('SELECT * FROM notes WHERE trip_id = ? ORDER BY created_at DESC', (trip_id,))
    trip['notes'] = [dict_from_row(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify({'trip': trip})

@app.route('/api/trips', methods=['POST'])
@login_required
def create_trip():
    """Create a new trip"""
    data = request.json
    user_id = request.user['id']
    
    if not data.get('name'):
        return jsonify({'error': 'Trip name is required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    share_code = secrets.token_urlsafe(8)
    
    cursor.execute('''
        INSERT INTO trips (user_id, name, description, start_date, end_date, cover_image, budget, currency, is_public, share_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        data['name'],
        data.get('description', ''),
        data.get('start_date'),
        data.get('end_date'),
        data.get('cover_image', ''),
        data.get('budget', 0),
        data.get('currency', 'USD'),
        data.get('is_public', 0),
        share_code
    ))
    
    trip_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute('SELECT * FROM trips WHERE id = ?', (trip_id,))
    trip = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Trip created', 'trip': trip}), 201

@app.route('/api/trips/<int:trip_id>', methods=['PUT'])
@login_required
def update_trip(trip_id):
    """Update a trip"""
    data = request.json
    user_id = request.user['id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check ownership
    cursor.execute('SELECT id FROM trips WHERE id = ? AND user_id = ?', (trip_id, user_id))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Trip not found'}), 404
    
    allowed_fields = ['name', 'description', 'start_date', 'end_date', 'cover_image', 'budget', 'currency', 'is_public', 'status']
    updates = []
    values = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f'{field} = ?')
            values.append(data[field])
    
    if updates:
        values.append(trip_id)
        cursor.execute(f'''
            UPDATE trips SET {', '.join(updates)}, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', values)
        conn.commit()
    
    cursor.execute('SELECT * FROM trips WHERE id = ?', (trip_id,))
    trip = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Trip updated', 'trip': trip})

@app.route('/api/trips/<int:trip_id>', methods=['DELETE'])
@login_required
def delete_trip(trip_id):
    """Delete a trip"""
    user_id = request.user['id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT id FROM trips WHERE id = ? AND user_id = ?', (trip_id, user_id))
    if not cursor.fetchone():
        conn.close()
        return jsonify({'error': 'Trip not found'}), 404
    
    cursor.execute('DELETE FROM trips WHERE id = ?', (trip_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Trip deleted'})

# ============== STOPS ROUTES ==============

@app.route('/api/trips/<int:trip_id>/stops', methods=['GET'])
@login_required
def get_stops(trip_id):
    """Get all stops for a trip"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM stops WHERE trip_id = ? ORDER BY order_index', (trip_id,))
    stops = [dict_from_row(row) for row in cursor.fetchall()]
    
    for stop in stops:
        cursor.execute('SELECT * FROM activities WHERE stop_id = ? ORDER BY order_index', (stop['id'],))
        stop['activities'] = [dict_from_row(row) for row in cursor.fetchall()]
    
    conn.close()
    return jsonify({'stops': stops})

@app.route('/api/trips/<int:trip_id>/stops', methods=['POST'])
@login_required
def create_stop(trip_id):
    """Add a stop to a trip"""
    data = request.json
    
    if not data.get('city'):
        return jsonify({'error': 'City is required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get next order index
    cursor.execute('SELECT MAX(order_index) as max_order FROM stops WHERE trip_id = ?', (trip_id,))
    result = cursor.fetchone()
    order_index = (result['max_order'] or 0) + 1
    
    cursor.execute('''
        INSERT INTO stops (trip_id, city, country, start_date, end_date, order_index, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        trip_id,
        data['city'],
        data.get('country', ''),
        data.get('start_date'),
        data.get('end_date'),
        order_index,
        data.get('notes', '')
    ))
    
    stop_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute('SELECT * FROM stops WHERE id = ?', (stop_id,))
    stop = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Stop added', 'stop': stop}), 201

@app.route('/api/stops/<int:stop_id>', methods=['PUT'])
@login_required
def update_stop(stop_id):
    """Update a stop"""
    data = request.json
    
    conn = get_db()
    cursor = conn.cursor()
    
    allowed_fields = ['city', 'country', 'start_date', 'end_date', 'order_index', 'notes']
    updates = []
    values = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f'{field} = ?')
            values.append(data[field])
    
    if updates:
        values.append(stop_id)
        cursor.execute(f'UPDATE stops SET {", ".join(updates)} WHERE id = ?', values)
        conn.commit()
    
    cursor.execute('SELECT * FROM stops WHERE id = ?', (stop_id,))
    stop = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Stop updated', 'stop': stop})

@app.route('/api/stops/<int:stop_id>', methods=['DELETE'])
@login_required
def delete_stop(stop_id):
    """Delete a stop"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM stops WHERE id = ?', (stop_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Stop deleted'})

# ============== ACTIVITIES ROUTES ==============

@app.route('/api/stops/<int:stop_id>/activities', methods=['POST'])
@login_required
def create_activity(stop_id):
    """Add activity to a stop"""
    data = request.json
    
    if not data.get('name'):
        return jsonify({'error': 'Activity name is required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT MAX(order_index) as max_order FROM activities WHERE stop_id = ?', (stop_id,))
    result = cursor.fetchone()
    order_index = (result['max_order'] or 0) + 1
    
    cursor.execute('''
        INSERT INTO activities (stop_id, name, category, description, location, date, time, duration, cost, is_booked, booking_reference, order_index)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        stop_id,
        data['name'],
        data.get('category', 'sightseeing'),
        data.get('description', ''),
        data.get('location', ''),
        data.get('date'),
        data.get('time', ''),
        data.get('duration', ''),
        data.get('cost', 0),
        data.get('is_booked', 0),
        data.get('booking_reference', ''),
        order_index
    ))
    
    activity_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute('SELECT * FROM activities WHERE id = ?', (activity_id,))
    activity = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Activity added', 'activity': activity}), 201

@app.route('/api/activities/<int:activity_id>', methods=['PUT'])
@login_required
def update_activity(activity_id):
    """Update an activity"""
    data = request.json
    
    conn = get_db()
    cursor = conn.cursor()
    
    allowed_fields = ['name', 'category', 'description', 'location', 'date', 'time', 'duration', 'cost', 'is_booked', 'booking_reference', 'order_index']
    updates = []
    values = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f'{field} = ?')
            values.append(data[field])
    
    if updates:
        values.append(activity_id)
        cursor.execute(f'UPDATE activities SET {", ".join(updates)} WHERE id = ?', values)
        conn.commit()
    
    cursor.execute('SELECT * FROM activities WHERE id = ?', (activity_id,))
    activity = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Activity updated', 'activity': activity})

@app.route('/api/activities/<int:activity_id>', methods=['DELETE'])
@login_required
def delete_activity(activity_id):
    """Delete an activity"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM activities WHERE id = ?', (activity_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Activity deleted'})

# ============== BUDGET ROUTES ==============

@app.route('/api/trips/<int:trip_id>/budget', methods=['GET'])
@login_required
def get_budget(trip_id):
    """Get budget items for a trip"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM budget_items WHERE trip_id = ? ORDER BY date DESC', (trip_id,))
    items = [dict_from_row(row) for row in cursor.fetchall()]
    
    # Calculate totals
    cursor.execute('SELECT SUM(amount) as total FROM budget_items WHERE trip_id = ?', (trip_id,))
    total = cursor.fetchone()['total'] or 0
    
    cursor.execute('SELECT category, SUM(amount) as total FROM budget_items WHERE trip_id = ? GROUP BY category', (trip_id,))
    by_category = {row['category']: row['total'] for row in cursor.fetchall()}
    
    conn.close()
    return jsonify({'items': items, 'total': total, 'by_category': by_category})

@app.route('/api/trips/<int:trip_id>/budget', methods=['POST'])
@login_required
def add_budget_item(trip_id):
    """Add budget item"""
    data = request.json
    
    if not data.get('category') or not data.get('amount'):
        return jsonify({'error': 'Category and amount are required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO budget_items (trip_id, category, description, amount, currency, is_paid, date)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        trip_id,
        data['category'],
        data.get('description', ''),
        data['amount'],
        data.get('currency', 'USD'),
        data.get('is_paid', 0),
        data.get('date')
    ))
    
    item_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute('SELECT * FROM budget_items WHERE id = ?', (item_id,))
    item = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Budget item added', 'item': item}), 201

@app.route('/api/budget/<int:item_id>', methods=['DELETE'])
@login_required
def delete_budget_item(item_id):
    """Delete budget item"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM budget_items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Budget item deleted'})

# ============== PACKING LIST ROUTES ==============

@app.route('/api/trips/<int:trip_id>/packing', methods=['GET'])
@login_required
def get_packing_list(trip_id):
    """Get packing list for a trip"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM packing_items WHERE trip_id = ? ORDER BY category, name', (trip_id,))
    items = [dict_from_row(row) for row in cursor.fetchall()]
    
    # Calculate progress
    total = len(items)
    packed = len([i for i in items if i['is_packed']])
    
    conn.close()
    return jsonify({'items': items, 'total': total, 'packed': packed})

@app.route('/api/trips/<int:trip_id>/packing', methods=['POST'])
@login_required
def add_packing_item(trip_id):
    """Add packing item"""
    data = request.json
    
    if not data.get('name'):
        return jsonify({'error': 'Item name is required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO packing_items (trip_id, name, category, quantity, is_packed)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        trip_id,
        data['name'],
        data.get('category', 'essentials'),
        data.get('quantity', 1),
        data.get('is_packed', 0)
    ))
    
    item_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute('SELECT * FROM packing_items WHERE id = ?', (item_id,))
    item = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Item added', 'item': item}), 201

@app.route('/api/packing/<int:item_id>', methods=['PUT'])
@login_required
def update_packing_item(item_id):
    """Update packing item (toggle packed status)"""
    data = request.json
    
    conn = get_db()
    cursor = conn.cursor()
    
    allowed_fields = ['name', 'category', 'quantity', 'is_packed']
    updates = []
    values = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f'{field} = ?')
            values.append(data[field])
    
    if updates:
        values.append(item_id)
        cursor.execute(f'UPDATE packing_items SET {", ".join(updates)} WHERE id = ?', values)
        conn.commit()
    
    cursor.execute('SELECT * FROM packing_items WHERE id = ?', (item_id,))
    item = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Item updated', 'item': item})

@app.route('/api/packing/<int:item_id>', methods=['DELETE'])
@login_required
def delete_packing_item(item_id):
    """Delete packing item"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM packing_items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Item deleted'})

# ============== NOTES ROUTES ==============

@app.route('/api/trips/<int:trip_id>/notes', methods=['GET'])
@login_required
def get_notes(trip_id):
    """Get notes for a trip"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM notes WHERE trip_id = ? ORDER BY created_at DESC', (trip_id,))
    notes = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'notes': notes})

@app.route('/api/trips/<int:trip_id>/notes', methods=['POST'])
@login_required
def create_note(trip_id):
    """Create a note"""
    data = request.json
    
    if not data.get('title'):
        return jsonify({'error': 'Note title is required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO notes (trip_id, stop_id, title, content, mood, images)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        trip_id,
        data.get('stop_id'),
        data['title'],
        data.get('content', ''),
        data.get('mood', ''),
        json.dumps(data.get('images', []))
    ))
    
    note_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    note = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Note created', 'note': note}), 201

@app.route('/api/notes/<int:note_id>', methods=['PUT'])
@login_required
def update_note(note_id):
    """Update a note"""
    data = request.json
    
    conn = get_db()
    cursor = conn.cursor()
    
    allowed_fields = ['title', 'content', 'mood', 'stop_id']
    updates = ['updated_at = CURRENT_TIMESTAMP']
    values = []
    
    for field in allowed_fields:
        if field in data:
            updates.append(f'{field} = ?')
            values.append(data[field])
    
    if 'images' in data:
        updates.append('images = ?')
        values.append(json.dumps(data['images']))
    
    values.append(note_id)
    cursor.execute(f'UPDATE notes SET {", ".join(updates)} WHERE id = ?', values)
    conn.commit()
    
    cursor.execute('SELECT * FROM notes WHERE id = ?', (note_id,))
    note = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Note updated', 'note': note})

@app.route('/api/notes/<int:note_id>', methods=['DELETE'])
@login_required
def delete_note(note_id):
    """Delete a note"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM notes WHERE id = ?', (note_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Note deleted'})

# ============== SAVED DESTINATIONS ROUTES ==============

@app.route('/api/destinations/saved', methods=['GET'])
@login_required
def get_saved_destinations():
    """Get user's saved destinations"""
    user_id = request.user['id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM saved_destinations WHERE user_id = ? ORDER BY created_at DESC', (user_id,))
    destinations = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'destinations': destinations})

@app.route('/api/destinations/saved', methods=['POST'])
@login_required
def save_destination():
    """Save a destination"""
    data = request.json
    user_id = request.user['id']
    
    if not data.get('city'):
        return jsonify({'error': 'City is required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO saved_destinations (user_id, city, country, region, image)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        user_id,
        data['city'],
        data.get('country', ''),
        data.get('region', ''),
        data.get('image', '')
    ))
    
    dest_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute('SELECT * FROM saved_destinations WHERE id = ?', (dest_id,))
    destination = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Destination saved', 'destination': destination}), 201

@app.route('/api/destinations/saved/<int:dest_id>', methods=['DELETE'])
@login_required
def remove_saved_destination(dest_id):
    """Remove saved destination"""
    user_id = request.user['id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM saved_destinations WHERE id = ? AND user_id = ?', (dest_id, user_id))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'Destination removed'})

# ============== PUBLIC/SHARED ROUTES ==============

@app.route('/api/trips/shared/<share_code>', methods=['GET'])
def get_shared_trip(share_code):
    """Get publicly shared trip (no auth required)"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM trips WHERE share_code = ? AND is_public = 1', (share_code,))
    trip = dict_from_row(cursor.fetchone())
    
    if not trip:
        conn.close()
        return jsonify({'error': 'Trip not found or not public'}), 404
    
    # Get stops with activities
    cursor.execute('SELECT * FROM stops WHERE trip_id = ? ORDER BY order_index', (trip['id'],))
    stops = [dict_from_row(row) for row in cursor.fetchall()]
    
    for stop in stops:
        cursor.execute('SELECT * FROM activities WHERE stop_id = ? ORDER BY order_index', (stop['id'],))
        stop['activities'] = [dict_from_row(row) for row in cursor.fetchall()]
    
    trip['stops'] = stops
    
    # Get owner info (limited)
    cursor.execute('SELECT id, name, avatar FROM users WHERE id = ?', (trip['user_id'],))
    trip['owner'] = dict_from_row(cursor.fetchone())
    
    conn.close()
    return jsonify({'trip': trip})

@app.route('/api/trips/<int:trip_id>/copy', methods=['POST'])
@login_required
def copy_trip(trip_id):
    """Copy a public trip to user's trips"""
    user_id = request.user['id']
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Get original trip
    cursor.execute('SELECT * FROM trips WHERE id = ? AND is_public = 1', (trip_id,))
    original = dict_from_row(cursor.fetchone())
    
    if not original:
        conn.close()
        return jsonify({'error': 'Trip not found or not public'}), 404
    
    # Create copy
    share_code = secrets.token_urlsafe(8)
    cursor.execute('''
        INSERT INTO trips (user_id, name, description, start_date, end_date, cover_image, budget, currency, share_code)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        user_id,
        f"{original['name']} (Copy)",
        original['description'],
        original['start_date'],
        original['end_date'],
        original['cover_image'],
        original['budget'],
        original['currency'],
        share_code
    ))
    
    new_trip_id = cursor.lastrowid
    
    # Copy stops and activities
    cursor.execute('SELECT * FROM stops WHERE trip_id = ? ORDER BY order_index', (trip_id,))
    stops = cursor.fetchall()
    
    for stop in stops:
        cursor.execute('''
            INSERT INTO stops (trip_id, city, country, start_date, end_date, order_index, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (new_trip_id, stop['city'], stop['country'], stop['start_date'], stop['end_date'], stop['order_index'], stop['notes']))
        
        new_stop_id = cursor.lastrowid
        
        cursor.execute('SELECT * FROM activities WHERE stop_id = ?', (stop['id'],))
        activities = cursor.fetchall()
        
        for activity in activities:
            cursor.execute('''
                INSERT INTO activities (stop_id, name, category, description, location, date, time, duration, cost, order_index)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (new_stop_id, activity['name'], activity['category'], activity['description'], activity['location'], 
                  activity['date'], activity['time'], activity['duration'], activity['cost'], activity['order_index']))
    
    conn.commit()
    
    cursor.execute('SELECT * FROM trips WHERE id = ?', (new_trip_id,))
    new_trip = dict_from_row(cursor.fetchone())
    conn.close()
    
    return jsonify({'message': 'Trip copied successfully', 'trip': new_trip}), 201

# ============== ADMIN ROUTES ==============

@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def get_admin_stats():
    """Get admin dashboard statistics"""
    conn = get_db()
    cursor = conn.cursor()
    
    # User stats
    cursor.execute('SELECT COUNT(*) as count FROM users')
    total_users = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM users WHERE created_at > datetime("now", "-7 days")')
    new_users_week = cursor.fetchone()['count']
    
    # Trip stats
    cursor.execute('SELECT COUNT(*) as count FROM trips')
    total_trips = cursor.fetchone()['count']
    
    cursor.execute('SELECT COUNT(*) as count FROM trips WHERE is_public = 1')
    public_trips = cursor.fetchone()['count']
    
    # Top destinations
    cursor.execute('''
        SELECT city, country, COUNT(*) as count 
        FROM stops 
        GROUP BY city, country 
        ORDER BY count DESC 
        LIMIT 10
    ''')
    top_destinations = [dict_from_row(row) for row in cursor.fetchall()]
    
    # Recent users
    cursor.execute('SELECT id, name, email, created_at FROM users ORDER BY created_at DESC LIMIT 10')
    recent_users = [dict_from_row(row) for row in cursor.fetchall()]
    
    # Activity by category
    cursor.execute('SELECT category, COUNT(*) as count FROM activities GROUP BY category')
    activity_stats = {row['category']: row['count'] for row in cursor.fetchall()}
    
    conn.close()
    
    return jsonify({
        'total_users': total_users,
        'new_users_week': new_users_week,
        'total_trips': total_trips,
        'public_trips': public_trips,
        'top_destinations': top_destinations,
        'recent_users': recent_users,
        'activity_stats': activity_stats
    })

@app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_all_users():
    """Get all users (admin only)"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT u.id, u.name, u.email, u.avatar, u.is_admin, u.created_at,
               (SELECT COUNT(*) FROM trips WHERE user_id = u.id) as trip_count
        FROM users u
        ORDER BY u.created_at DESC
    ''')
    users = [dict_from_row(row) for row in cursor.fetchall()]
    conn.close()
    
    return jsonify({'users': users})

@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """Delete a user (admin only)"""
    if user_id == request.user['id']:
        return jsonify({'error': 'Cannot delete yourself'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'message': 'User deleted'})

# ============== SEARCH ROUTES ==============

@app.route('/api/search/cities', methods=['GET'])
@login_required
def search_cities():
    """Search cities - returns mock data"""
    query = request.args.get('q', '').lower()
    region = request.args.get('region', '')
    
    # Mock cities data
    cities = [
        {'city': 'Paris', 'country': 'France', 'region': 'Europe', 'image': 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=400'},
        {'city': 'Tokyo', 'country': 'Japan', 'region': 'Asia', 'image': 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=400'},
        {'city': 'New York', 'country': 'USA', 'region': 'North America', 'image': 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?w=400'},
        {'city': 'London', 'country': 'UK', 'region': 'Europe', 'image': 'https://images.unsplash.com/photo-1513635269975-59663e0ac1ad?w=400'},
        {'city': 'Sydney', 'country': 'Australia', 'region': 'Oceania', 'image': 'https://images.unsplash.com/photo-1506973035872-a4ec16b8e8d9?w=400'},
        {'city': 'Dubai', 'country': 'UAE', 'region': 'Middle East', 'image': 'https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=400'},
        {'city': 'Singapore', 'country': 'Singapore', 'region': 'Asia', 'image': 'https://images.unsplash.com/photo-1525625293386-3f8f99389edd?w=400'},
        {'city': 'Barcelona', 'country': 'Spain', 'region': 'Europe', 'image': 'https://images.unsplash.com/photo-1583422409516-2895a77efded?w=400'},
        {'city': 'Rome', 'country': 'Italy', 'region': 'Europe', 'image': 'https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=400'},
        {'city': 'Bali', 'country': 'Indonesia', 'region': 'Asia', 'image': 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?w=400'},
        {'city': 'Cape Town', 'country': 'South Africa', 'region': 'Africa', 'image': 'https://images.unsplash.com/photo-1580060839134-75a5edca2e99?w=400'},
        {'city': 'Rio de Janeiro', 'country': 'Brazil', 'region': 'South America', 'image': 'https://images.unsplash.com/photo-1483729558449-99ef09a8c325?w=400'},
    ]
    
    results = cities
    if query:
        results = [c for c in results if query in c['city'].lower() or query in c['country'].lower()]
    if region:
        results = [c for c in results if c['region'] == region]
    
    return jsonify({'cities': results})

@app.route('/api/search/activities', methods=['GET'])
@login_required
def search_activities():
    """Search activities - returns mock data"""
    category = request.args.get('category', '')
    
    # Mock activities data
    activities = [
        {'name': 'Eiffel Tower Visit', 'category': 'sightseeing', 'location': 'Paris', 'cost': 25},
        {'name': 'Louvre Museum', 'category': 'sightseeing', 'location': 'Paris', 'cost': 17},
        {'name': 'French Cooking Class', 'category': 'food', 'location': 'Paris', 'cost': 120},
        {'name': 'Sushi Making Workshop', 'category': 'food', 'location': 'Tokyo', 'cost': 80},
        {'name': 'Mount Fuji Hike', 'category': 'adventure', 'location': 'Tokyo', 'cost': 150},
        {'name': 'Central Park Walk', 'category': 'sightseeing', 'location': 'New York', 'cost': 0},
        {'name': 'Broadway Show', 'category': 'entertainment', 'location': 'New York', 'cost': 150},
        {'name': 'Scuba Diving', 'category': 'adventure', 'location': 'Bali', 'cost': 100},
        {'name': 'Temple Tour', 'category': 'sightseeing', 'location': 'Bali', 'cost': 50},
        {'name': 'Safari Tour', 'category': 'adventure', 'location': 'Cape Town', 'cost': 200},
        {'name': 'Wine Tasting', 'category': 'food', 'location': 'Cape Town', 'cost': 75},
        {'name': 'Colosseum Tour', 'category': 'sightseeing', 'location': 'Rome', 'cost': 20},
    ]
    
    results = activities
    if category:
        results = [a for a in results if a['category'] == category]
    
    return jsonify({'activities': results})

# ============== ERROR HANDLERS ==============

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

# ============== MAIN ==============

if __name__ == '__main__':
    init_db()
    
    # Create admin user if not exists
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE email = ?', ('admin@traveloop.com',))
    if not cursor.fetchone():
        admin_hash = hash_password('admin123')
        cursor.execute('''
            INSERT INTO users (name, email, password_hash, is_admin)
            VALUES (?, ?, ?, ?)
        ''', ('Admin', 'admin@traveloop.com', admin_hash, 1))
        conn.commit()
        print("Admin user created: admin@traveloop.com / admin123")
    conn.close()
    
    print("Starting Traveloop Backend Server...")
    print("API running at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
