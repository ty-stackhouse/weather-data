# server_manager.py
# Manages the lifecycle of the Flask server process
# Used by the test script to start and stop the server programmatically

import subprocess
import time
import socket
import atexit

# Global variable to hold the server process
_server_process = None


def _is_port_open(port):
    """Check if a given port is open."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def start_server():
    """Start the Flask server and wait for it to be ready."""
    global _server_process
    
    # Start the Flask application
    _server_process = subprocess.Popen(['python', 'app.py'])
    
    # Wait for the server to start listening on port 5000
    max_wait = 10  # seconds
    wait_interval = 0.5
    elapsed = 0
    
    while not _is_port_open(5000) and elapsed < max_wait:
        time.sleep(wait_interval)
        elapsed += wait_interval
    
    if not _is_port_open(5000):
        raise RuntimeError('Server failed to start on port 5000')
    
    print("Server started on http://localhost:5000")


def stop_server():
    """Stop the Flask server gracefully."""
    global _server_process
    
    if _server_process:
        print("Stopping server...")
        _server_process.terminate()
        try:
            _server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            _server_process.kill()
        _server_process = None
        print("Server stopped.")

# Register cleanup function to ensure server is stopped
atexit.register(stop_server)