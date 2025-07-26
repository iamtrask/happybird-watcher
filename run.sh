#!/bin/bash
set -e

# SyftBox app runner for happybird-watcher
# This script is executed by SyftBox when the app is deployed

echo "Starting happybird-watcher SyftBox app..."

# Get assigned port from SyftBox or use default
SYFTBOX_ASSIGNED_PORT=${SYFTBOX_ASSIGNED_PORT:-8005}
echo "Using port: $SYFTBOX_ASSIGNED_PORT"

# Save port to config file for discovery
CONFIG_DIR="$HOME/.happybird-watcher"
mkdir -p "$CONFIG_DIR"
echo "{"port": $SYFTBOX_ASSIGNED_PORT}" > "$CONFIG_DIR/config.json"
echo "Saved port configuration to $CONFIG_DIR/config.json"

# Environment setup for clean installation
export ZSH_DISABLE_COMPFIX=true
export NONINTERACTIVE=1

# Create fresh virtual environment with UV
echo "Setting up Python environment..."
rm -rf .venv
uv venv --python 3.12
export VIRTUAL_ENV="$(pwd)/.venv"
export PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
echo "Installing dependencies..."
# First install syft-widget from local path
uv pip install -e /Users/atrask/Desktop/Laboratory/syft-widget
# Then sync other dependencies
uv sync
# Install the current package
uv pip install -e .

# Use fixed discovery port for debugging
DISCOVERY_PORT=62050
echo "Using discovery port: $DISCOVERY_PORT"

# Find and kill any process running on the discovery port to prevent conflicts
echo "Checking for and terminating any existing process on port $DISCOVERY_PORT..."
PID_TO_KILL=$(lsof -t -i:$DISCOVERY_PORT || true)
if [ -n "$PID_TO_KILL" ]; then
    echo "Found existing process(es) with PID(s): $PID_TO_KILL. Terminating..."
    kill -9 $PID_TO_KILL
    sleep 1 # Give it a moment to release the port
    echo "Process(es) terminated."
else
    echo "No existing process found on port $DISCOVERY_PORT."
fi

# Start discovery server in background
echo "Starting discovery server on port $DISCOVERY_PORT..."
uv run python -c "
import json
from http.server import HTTPServer, BaseHTTPRequestHandler

class DiscoveryHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        self.end_headers()
        response = {'main_server_port': $SYFTBOX_ASSIGNED_PORT, 'discovery_port': $DISCOVERY_PORT}
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        pass  # Suppress logging

server = HTTPServer(('0.0.0.0', $DISCOVERY_PORT), DiscoveryHandler)
server.serve_forever()
" &

DISCOVERY_PID=$!
echo "Discovery server started with PID $DISCOVERY_PID"

# Launch the syft-widget server for happybird-watcher
echo "Launching happybird-watcher widget server on port $SYFTBOX_ASSIGNED_PORT..."
export SYFTBOX_PORT=$SYFTBOX_ASSIGNED_PORT
export DISCOVERY_PORT=$DISCOVERY_PORT

# Add syft-widget to Python path and start the server
export PYTHONPATH="/Users/atrask/Desktop/Laboratory/syft-widget:$PYTHONPATH"

# Start the syft-widget server with auto-discovery of endpoints
uv run python -m syft_widget.cli \
    --package-name "happybird_watcher" \
    --package-dir "$(pwd)" \
    --auto-discover \
    --port $SYFTBOX_ASSIGNED_PORT
