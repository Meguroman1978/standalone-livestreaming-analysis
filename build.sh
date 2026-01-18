#!/bin/bash

# Build script for Render.com
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Creating upload directory..."
mkdir -p static/uploads

echo "Build completed successfully!"
