#!/bin/bash
echo "=== Starting Alchemist App ==="
echo "PWD: $(pwd)"
echo "Files in /app:"
ls -la /app 2>/dev/null || echo "/app not found"
echo "Files in current dir:"
ls -la
echo "Python version:"
python --version
echo "Starting uvicorn..."
cd /app
uvicorn src.main:app --host 0.0.0.0 --port ${PORT:-8080}
