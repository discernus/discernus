#!/bin/bash
# Local Development Setup Script for Discernus
# Switches from Docker-first to local development with validation

set -e

echo "🏗️  Setting up Discernus for Local Development"
echo "=============================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: Run this script from the Discernus project root"
    exit 1
fi

# 1. Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# 2. Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate || {
    echo "❌ Failed to activate virtual environment"
    exit 1
}

# 3. Upgrade pip
echo "📈 Upgrading pip..."
pip install --upgrade pip

# 4. Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# 5. Set up environment file
if [ ! -f ".env" ]; then
    echo "⚙️  Setting up environment configuration..."
    cp env.example .env
    echo "✅ Created .env from env.example"
    echo "📝 Please edit .env to configure your local database"
else
    echo "✅ .env already exists"
fi

# 6. Check Python path
echo "🐍 Python environment:"
which python3
python3 --version

# 7. Verify installation
echo "🧪 Testing installation..."
if python3 -c "import numpy, pandas, pytest; print('✅ Core dependencies available')"; then
    echo "✅ Installation successful"
else
    echo "❌ Installation verification failed"
    exit 1
fi

# 8. Run a quick test
echo "🔬 Running quick test suite..."
if python3 -m pytest tests/unit/test_discernus_coordinate_system.py -v --tb=short; then
    echo "✅ Tests passing - ready for development!"
else
    echo "⚠️  Some tests failed, but environment is set up"
fi

echo ""
echo "🎉 Local development setup complete!"
echo ""
echo "Next steps:"
echo "1. source venv/bin/activate"
echo "2. Edit .env for your database configuration"
echo "3. python3 -m pytest tests/unit/ -v"
echo "4. Start developing!"
echo ""
echo "💡 Remember: Validate in Docker before committing:"
echo "   docker-compose up -d && docker-compose run --rm app python3 -m pytest tests/unit/ -v" 