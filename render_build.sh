#!/usr/bin/env bash
# Build script for Render deployment
set -e

echo "=== Installing Python dependencies ==="
pip install -r requirements.txt

echo "=== Installing Node.js dependencies ==="
cd frontend
npm install
npm run build
cd ..

echo "=== Running corpus ingestion ==="
python scripts/ingest.py

echo "=== Build complete ==="
