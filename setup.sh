#!/bin/bash
echo "Installing dependencies..."

# It's recommended to run this in a virtual environment
# python3 -m venv venv
# source venv/bin/activate

pip install -r requirements.txt

echo "Dependencies installed."
echo "To run the application, first set your Google API Key:"
echo "export GOOGLE_API_KEY='your_api_key_here'"
echo "Then, run the main application:"
echo "python3 main.py"
