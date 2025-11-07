#!/bin/bash
# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Start backend in background
echo "Starting backend server on port 8080..."
cd backend
source venv/bin/activate
python main.py > ../backend.log 2>&1 &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend
echo "Starting frontend server on port 3000..."
cd "$SCRIPT_DIR/frontend"
HOST_VALUE="${HOST:-0.0.0.0}"
PORT_VALUE="${PORT:-3000}"

HOST="$HOST_VALUE" PORT="$PORT_VALUE" npm run dev -- --host "$HOST_VALUE" --port "$PORT_VALUE"

# Cleanup on exit
trap "kill $BACKEND_PID 2>/dev/null" EXIT
