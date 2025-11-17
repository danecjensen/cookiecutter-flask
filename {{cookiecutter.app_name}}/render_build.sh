#!/usr/bin/env bash
# Render.com build script
set -o errexit  # Exit on error

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Install Node.js dependencies and build frontend assets
npm install
npm run build

# Run database migrations
flask db upgrade
