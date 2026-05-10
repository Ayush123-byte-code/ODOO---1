#!/usr/bin/env python3
"""
Traveloop Backend Runner
Quick script to setup and run the Flask backend
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_cors
        print("Dependencies already installed.")
        return True
    except ImportError:
        return False

def install_dependencies():
    """Install required packages"""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Dependencies installed successfully!")

def run_server():
    """Run the Flask server"""
    print("\n" + "="*50)
    print("Starting Traveloop Backend Server")
    print("="*50)
    print("\nServer running at: http://localhost:5000")
    print("API Base URL: http://localhost:5000/api")
    print("\nDefault Admin Credentials:")
    print("  Email: admin@traveloop.com")
    print("  Password: admin123")
    print("\nPress Ctrl+C to stop the server")
    print("="*50 + "\n")
    
    # Run the app
    from app import app, init_db
    
    # Initialize database
    init_db()
    
    # Create admin if not exists
    from app import get_db, hash_password
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
        print("Admin user created!")
    conn.close()
    
    # Run server
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    if not check_dependencies():
        install_dependencies()
    
    run_server()
