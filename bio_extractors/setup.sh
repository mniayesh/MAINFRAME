#!/bin/bash

# Biological Database Extraction Framework Setup Script
# This script sets up the environment and verifies dependencies

echo "=================================="
echo "BioExtractors Setup"
echo "=================================="

# Check Python version
echo -e "\n1. Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
REQUIRED_VERSION="3.8.0"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" = "$REQUIRED_VERSION" ]; then
    echo "   ✓ Python $PYTHON_VERSION (>= $REQUIRED_VERSION required)"
else
    echo "   ✗ Python $PYTHON_VERSION found, but >= $REQUIRED_VERSION required"
    exit 1
fi

# Create virtual environment
echo -e "\n2. Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✓ Virtual environment created"
else
    echo "   ✓ Virtual environment already exists"
fi

# Activate virtual environment
echo -e "\n3. Activating virtual environment..."
source venv/bin/activate
echo "   ✓ Virtual environment activated"

# Upgrade pip
echo -e "\n4. Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "   ✓ pip upgraded"

# Install dependencies
echo -e "\n5. Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "   ✓ Dependencies installed"
else
    echo "   ✗ Error installing dependencies"
    exit 1
fi

# Create directories
echo -e "\n6. Creating directories..."
mkdir -p .cache
mkdir -p extraction_results
mkdir -p logs
echo "   ✓ Directories created"

# Verify imports
echo -e "\n7. Verifying installation..."
python3 -c "from bio_extractors import GOExtractor; print('   ✓ bio_extractors imports successfully')" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "   ✗ Import verification failed"
    exit 1
fi

# Check database schema
echo -e "\n8. Checking database schema..."
if [ -f "../bio_architecture_schema.sql" ]; then
    echo "   ✓ Database schema found"
else
    echo "   ⚠ Database schema not found at ../bio_architecture_schema.sql"
fi

# Configuration check
echo -e "\n9. Checking configuration..."
if [ -f "config/extraction_config.yaml" ]; then
    echo "   ✓ Configuration file found"
else
    echo "   ✗ Configuration file not found"
    exit 1
fi

# Summary
echo -e "\n=================================="
echo "Setup Complete!"
echo "=================================="
echo -e "\nNext steps:"
echo "  1. Activate the virtual environment:"
echo "     source venv/bin/activate"
echo ""
echo "  2. (Optional) Add credentials to config/extraction_config.yaml:"
echo "     - BRENDA email/password"
echo "     - BioPortal API key"
echo ""
echo "  3. Run example extraction:"
echo "     python example_usage.py"
echo ""
echo "  4. Or run full extraction:"
echo "     python extract_all.py --dry-run  # Preview"
echo "     python extract_all.py            # Execute"
echo ""
echo "  5. View README.md for detailed documentation"
echo ""
echo "=================================="
