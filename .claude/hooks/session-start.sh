#!/bin/bash
set -euo pipefail

# Session Start Hook: Install dependencies and configure environment
# This hook ensures pylint and other tools are available for code analysis

echo "🔧 Setting up Claude Code environment..."

# Install pylint for code analysis (non-optional)
echo "📦 Installing pylint..."
pip install -q pylint

# Install commonly used dependencies (these may already be installed)
echo "📦 Installing core dependencies..."
pip install -q \
  numpy \
  sympy \
  requests \
  beautifulsoup4 \
  scipy \
  2>/dev/null || echo "⚠️  Some optional packages failed to install (this is OK if already present)"

# Set PYTHONPATH to include current directory
if [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  echo 'export PYTHONPATH="${PYTHONPATH:+${PYTHONPATH}:}."' >> "$CLAUDE_ENV_FILE"
fi

# Verify pylint is installed
if command -v pylint &> /dev/null; then
  echo "✅ pylint is ready: $(pylint --version | head -1)"
else
  echo "❌ pylint installation failed!"
  exit 1
fi

echo "✅ Environment setup complete!"
