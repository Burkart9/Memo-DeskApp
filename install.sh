#!/bin/bash
echo "Installing Reminders Application dependencies..."
echo "Creating virtual environment..."
python3 -m venv venv
echo "Activating virtual environment..."
source venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Installation complete!"
echo "You can now run the application with: python main.py"
