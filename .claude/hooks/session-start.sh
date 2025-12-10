#!/bin/bash
set -euo pipefail

# Session Start Hook: Install dependencies, configure environment, and detect merge conflicts
# This hook ensures pylint and other tools are available, and notifies Claude of merge conflicts

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

# Check for merge conflicts
echo "🔍 Checking for merge conflicts..."

# Function to detect merge conflict markers
detect_conflicts() {
  local conflict_files=()

  # Check for files with conflict markers
  if grep -r --include="*.py" --include="*.json" --include="*.md" --include="*.txt" \
    "^<<<<<<< HEAD" . 2>/dev/null; then
    while IFS= read -r file; do
      conflict_files+=("$file")
    done < <(grep -l "^<<<<<<< HEAD" $(find . -type f \( -name "*.py" -o -name "*.json" -o -name "*.md" -o -name "*.txt" \) 2>/dev/null) 2>/dev/null || true)
  fi

  # Check git status for unmerged paths
  if command -v git &> /dev/null; then
    while IFS= read -r file; do
      if [[ -n "$file" ]]; then
        conflict_files+=("$file")
      fi
    done < <(git diff --name-only --diff-filter=U 2>/dev/null || true)
  fi

  # Report conflicts if found
  if [ ${#conflict_files[@]} -gt 0 ]; then
    echo ""
    echo "⚠️  MERGE CONFLICTS DETECTED!"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "The following files have merge conflicts:"
    printf '%s\n' "${conflict_files[@]}" | sort | uniq | while read -r f; do
      echo "  • $f"
    done
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "Please resolve these conflicts before proceeding."
    echo ""
    return 1
  else
    echo "✅ No merge conflicts found"
    return 0
  fi
}

# Run conflict detection
if ! detect_conflicts; then
  echo ""
  echo "CONFLICT RESOLUTION REQUIRED"
  echo "Please run: git status"
  echo "And resolve conflicts in the files listed above."
  exit 1
fi

echo "✅ Environment setup complete!"
