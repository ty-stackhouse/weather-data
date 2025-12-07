# app.py
# Flask web application server
# Serves the main page and a simple status API endpoint

from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder='.', static_url_path='')

@app.route('/')
def index():
    """Serve the main HTML page from the current directory."""
    return send_from_directory('.', 'index.html')

@app.route('/api/status')
def status():
    """API endpoint to check server status."""
    return {
        "status": "API Ready",
        "message": "System operational"
    }

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(port=5000, debug=False)