#!/bin/bash

# Script to run the Claims Management System with virtual environment activated

echo "🚀 Starting Claims Management System..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Creating one..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "📦 Activating virtual environment..."
source venv/bin/activate

# Check if requirements are installed
echo "🔍 Checking dependencies..."
if ! python -c "import reflex" 2>/dev/null; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
fi

# Check environment variables
echo "🔧 Checking environment variables..."
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

required_vars = [
    'DATABASE_URL',
    'GEMINI_API_KEY',
    'GOOGLE_CLOUD_PROJECT_ID',
    'GOOGLE_CLOUD_BUCKET_NAME',
    'GOOGLE_APPLICATION_CREDENTIALS_JSON',
    'GMAIL_CREDENTIALS_JSON',
    'GMAIL_TOKEN_JSON'
]

missing_vars = [var for var in required_vars if not os.getenv(var)]
if missing_vars:
    print('❌ Missing environment variables:')
    for var in missing_vars:
        print(f'   - {var}')
    print('\\n💡 Make sure to configure all variables in the .env file')
    exit(1)
else:
    print('✅ All environment variables are configured')
"

if [ $? -ne 0 ]; then
    echo "❌ Environment variables check failed"
    exit 1
fi

echo "✅ All checks passed"
echo "🌐 Starting Reflex application..."
echo "📱 Application will be available at: http://localhost:3000"
echo "⏹️  Press Ctrl+C to stop the server"

# Run the Reflex application
reflex run 