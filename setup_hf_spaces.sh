#!/bin/bash
# Quick setup script for Hugging Face Spaces deployment
# Usage: bash setup_hf_spaces.sh YOUR_USERNAME YOUR_SPACE_NAME

if [ $# -lt 2 ]; then
    echo "Usage: bash setup_hf_spaces.sh YOUR_USERNAME YOUR_SPACE_NAME"
    echo "Example: bash setup_hf_spaces.sh myusername financial-classifier"
    exit 1
fi

USERNAME=$1
SPACE_NAME=$2
SPACE_URL="https://huggingface.co/spaces/${USERNAME}/${SPACE_NAME}"

echo "🚀 Financial News Classifier - HF Spaces Setup"
echo "================================================"
echo ""
echo "Space URL: $SPACE_URL"
echo ""

# Step 1: Clone space
echo "📥 Step 1: Cloning your HF Space..."
git clone "https://huggingface.co/spaces/${USERNAME}/${SPACE_NAME}" hf_space_temp
cd hf_space_temp || exit 1

echo "✅ Space cloned successfully"
echo ""

# Step 2: Copy files
echo "📋 Step 2: Copying project files..."

# Create directory structure
mkdir -p src/core

# Copy necessary files
echo "   - Copying gui.py as app.py..."
cp ../src/gui.py app.py

echo "   - Copying core modules..."
cp ../src/core/infer.py src/core/
cp ../src/core/io_utils.py src/core/
cp ../src/core/rss.py src/core/

echo "   - Copying requirements.txt..."
cp ../requirements.txt .

echo "   - Copying README.md..."
cp ../README.md .

# Create __init__.py files
touch src/__init__.py
touch src/core/__init__.py

echo "✅ Files copied successfully"
echo ""

# Step 3: Create .gitignore
echo "🔧 Step 3: Creating .gitignore..."
cat > .gitignore << 'EOF'
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv
.env
*.egg-info/
dist/
build/
.cache/
.pytest_cache/
.huggingface/
*.log
.DS_Store
EOF
echo "✅ .gitignore created"
echo ""

# Step 4: Update imports in app.py
echo "⚙️  Step 4: Fixing import paths..."
sed -i 's/from src\.core\./from core\./g' app.py
echo "✅ Import paths fixed"
echo ""

# Step 5: Git operations
echo "📤 Step 5: Preparing to push..."
git add .
git commit -m "Initial deployment: Financial News Classifier to HF Spaces"

echo ""
echo "✅ All set up! Ready to push."
echo ""
echo "📝 Next steps:"
echo "   1. Review the changes in this directory"
echo "   2. Run: git push"
echo "   3. Enter your HF token when prompted"
echo "   4. Space will auto-build (2-5 minutes)"
echo "   5. Visit: $SPACE_URL"
echo ""
echo "❓ If you need to make changes:"
echo "   1. Edit files in this directory"
echo "   2. Run: git add . && git commit -m 'Your message' && git push"
echo ""
