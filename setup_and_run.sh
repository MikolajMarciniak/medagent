#!/bin/bash
# MedAgent Setup and Run Script
# This script installs dependencies, ingests medical data, and launches the ADK web server

echo "🏥 MedAgent Setup and Run Script"
echo "================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "❌ Error: .env file not found!"
    echo "Please copy .env.example to .env and configure your GOOGLE_API_KEY"
    exit 1
fi

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python --version 2>&1)
echo "   $python_version"

if ! echo "$python_version" | grep -qE "Python 3\.(1[0-9]|[2-9][0-9])"; then
    echo "❌ Python 3.10 or later is required!"
    exit 1
fi

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies!"
    exit 1
fi
echo "   ✅ Dependencies installed successfully"

# Check if knowledge base exists
if [ ! -d "data/chroma_db" ] && [ ! -d "datas/chroma_db" ]; then
    echo ""
    echo "📚 Downloading and ingesting medical knowledge base..."
    echo "   This may take a few minutes..."
    python scripts/ingest_data.py
    if [ $? -ne 0 ]; then
        echo "❌ Failed to ingest data!"
        exit 1
    fi
    echo "   ✅ Knowledge base ready"
else
    echo ""
    echo "✅ Knowledge base already exists, skipping ingestion"
fi

# Check if port 8000 is already in use
echo ""
echo "🔍 Checking if server is already running..."
if curl -sSf http://127.0.0.1:8000 >/dev/null 2>&1; then
  echo "✅ ADK server is already running at http://127.0.0.1:8000"
  echo "   Opening browser..."
  URL="http://127.0.0.1:8000"
  # Try platform-specific open commands
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$URL" >/dev/null 2>&1 &
  elif command -v open >/dev/null 2>&1; then
    open "$URL" >/dev/null 2>&1 &
  elif command -v start >/dev/null 2>&1; then
    start "$URL" >/dev/null 2>&1 &
  else
    # Git Bash on Windows often needs cmd.exe
    if command -v cmd.exe >/dev/null 2>&1; then
      cmd.exe /c start "$URL"
    else
      echo "👉 Please open $URL in your browser."
    fi
  fi
  echo ""
  echo "✨ Setup complete! The server was already running."
  exit 0
fi

# Launch ADK web server (background) and open browser
echo ""
echo "🚀 Starting ADK web server..."
echo "   Server will be available at: http://127.0.0.1:8000"
echo "   The browser will open automatically when ready."
echo "   Press Ctrl+C to stop and clean up."
echo ""

# Start the server in background and capture PID
nohup adk web --port 8000 > adk_server.out 2>&1 &
SERVER_PID=$!

# Ensure cleanup on exit
cleanup() {
  echo ""
  echo "🧹 Stopping ADK server (PID $SERVER_PID)..."
  kill "$SERVER_PID" 2>/dev/null || true
  wait "$SERVER_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

# Wait for server to be ready
echo "⏳ Waiting for server to become ready..."
READY=0
for i in $(seq 1 40); do
  if curl -sSf http://127.0.0.1:8000 >/dev/null 2>&1; then
    READY=1
    break
  fi
  sleep 0.5
doneif [ "$READY" = "1" ]; then
    echo "✅ Server is up. Opening browser..."
    URL="http://127.0.0.1:8000"
    # Try platform-specific open commands
    if command -v xdg-open >/dev/null 2>&1; then
        xdg-open "$URL" >/dev/null 2>&1 &
    elif command -v open >/dev/null 2>&1; then
        open "$URL" >/dev/null 2>&1 &
    elif command -v start >/dev/null 2>&1; then
        start "$URL" >/dev/null 2>&1 &
    else
        # Git Bash on Windows often needs cmd.exe
        if command -v cmd.exe >/dev/null 2>&1; then
            cmd.exe /c start "$URL"
        else
            echo "👉 Please open $URL in your browser."
        fi
    fi
else
    echo "❌ Server did not become ready in time. Logs:"
    tail -n +1 adk_server.out || true
    exit 1
fi

# Follow logs until interrupted
echo "📜 Streaming server logs. Press Ctrl+C to stop."
tail -f adk_server.out
