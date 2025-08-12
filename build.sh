#!/usr/bin/env bash
# Build script for Render deployment

echo "🚀 Starting build process..."

# Upgrade pip
pip install --upgrade pip

# Install wheel and setuptools first
pip install --upgrade wheel setuptools

# Install requirements
pip install -r requirements.txt

echo "✅ Build completed successfully!"
