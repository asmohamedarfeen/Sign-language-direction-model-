#!/usr/bin/env bash
# ==========================================================
# Run SignSpeak Full Stack Development Server
# ==========================================================

set -e

echo "Starting SignSpeak Backend..."
source .venv/bin/activate
export PYTHONPATH=.
python3 backend/main.py &
BACKEND_PID=$!

echo "Starting SignSpeak Frontend (Vite)..."
cd frontend
npm run dev -- --port 5173 &
FRONTEND_PID=$!

echo "=========================================================="
echo " SignSpeak Development Services Running!"
echo " Backend:  http://localhost:8000 (Docs: /docs)"
echo " Frontend: http://localhost:5173"
echo " Press Ctrl+C to terminate both servers."
echo "=========================================================="

trap "kill $BACKEND_PID $FRONTEND_PID; exit 0" SIGINT SIGTERM
wait
