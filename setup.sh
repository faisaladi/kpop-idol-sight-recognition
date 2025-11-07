#!/bin/bash
set -e

echo "🚀 Setting up K-POP Artist Recognizer..."

# Get the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
cd "$SCRIPT_DIR/frontend"
npm install

# Create Python virtual environment
echo "🐍 Creating Python virtual environment..."
cd "$SCRIPT_DIR/backend"
python3 -m venv venv

# Install backend dependencies
echo "📦 Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Add K-POP artists to the database:"
echo "   cd backend && source venv/bin/activate"
echo "   python add_artist.py 'Artist Name' 'Group Name' 'path/to/photo.jpg'"
echo "2. The server will start automatically"
echo ""
