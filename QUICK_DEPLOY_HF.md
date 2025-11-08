# Quick Start: HF Spaces Deployment

**Deploy Financial News Classifier to Hugging Face Spaces in 5 minutes!**

---

## Prerequisites

- ✅ Hugging Face account (free)
- ✅ Space created on HF website
- ✅ Git installed locally

---

## Quick Setup (Automated)

### Option 1: Using Setup Script (Easiest)

```bash
# Navigate to project directory
cd /home/tads/Work/TADS_PROJ/financial-news-classifier

# Run setup script
bash setup_hf_spaces.sh YOUR_USERNAME YOUR_SPACE_NAME

# Example:
bash setup_hf_spaces.sh myusername financial-classifier
```

Then in the generated `hf_space_temp` directory:
```bash
cd hf_space_temp
git push
```

---

## Manual Setup (Step-by-Step)

### Step 1: Clone Your Space
```bash
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
```

### Step 2: Copy Files
```bash
# From your project directory
cp path/to/src/gui.py app.py          # IMPORTANT: must be named app.py
cp path/to/src/core ./ -r             # Copy core module
cp path/to/requirements.txt .          # Copy dependencies
cp path/to/README.md .                 # Copy README
```

### Step 3: Fix Imports
Edit `app.py` and change all imports:
```python
# CHANGE THIS:
from src.core.infer import predict

# TO THIS:
from core.infer import predict
```

### Step 4: Verify Structure
```
YOUR_SPACE_NAME/
├── app.py                 ✅ Required
├── requirements.txt       ✅ Required
├── README.md             ✅ Recommended
└── core/
    ├── __init__.py
    ├── infer.py
    ├── io_utils.py
    └── rss.py
```

### Step 5: Commit and Push
```bash
git add .
git commit -m "Initial deployment: Financial News Classifier"
git push
```

**Enter your HF token when prompted** (get it from https://huggingface.co/settings/tokens)

---

## That's It! ✨

After pushing:
1. **Wait 2-5 minutes** for the Space to build
2. Visit: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`
3. Your app should be live!

---

## Troubleshooting Quick Fixes

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: No module named 'src'` | Remove `src.` from all imports in app.py |
| Build fails with model errors | Add `torch>=1.13.0` to requirements.txt |
| Takes too long to build | Check Logs tab; remove unnecessary packages |
| Port already in use | Spaces handles ports automatically |
| Import errors | Make sure core/ is in same directory as app.py |

---

## Making Updates

After deployment, to update your app:

```bash
# Make changes to files in your Space directory
# Then:
git add .
git commit -m "Update: describe your changes"
git push

# Space auto-rebuilds!
```

---

## What to Do With Your Space URL

Your Space URL is: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`

You can:
- ✅ Share this link directly (anyone can use it)
- ✅ Embed it on your website (Spaces provides embed code)
- ✅ Add to your portfolio
- ✅ Share on social media
- ✅ Use in production (within Spaces limits)

---

## Key Files for Spaces

**You must have these files:**
- `app.py` - Your Gradio interface (from gui.py)
- `requirements.txt` - Python dependencies

**Optional but recommended:**
- `README.md` - Space description
- `Dockerfile` - For custom setup

---

## Common Errors & Solutions

### ❌ "ModuleNotFoundError: No module named 'src'"

**Solution:** Your imports are wrong. In Spaces, remove `src.` prefix:

```python
# ❌ Wrong
from src.core.infer import predict

# ✅ Correct
from core.infer import predict
```

**To fix all at once:**
```bash
sed -i 's/from src\.core\./from core\./g' app.py
```

### ❌ Build takes forever or fails

**Solution:** Check requirements.txt for issues

```bash
# ❌ Too heavy
torch
transformers
tensorflow  # Don't include if not needed
scikit-learn
matplotlib

# ✅ Minimal
torch>=1.13.0
transformers>=4.25.0
gradio>=3.40.0
numpy>=1.23.0
pandas>=1.5.0
requests>=2.28.0
feedparser>=6.0.0
```

### ❌ "Could not find torch in dependencies"

**Solution:** Make sure torch is in requirements.txt with proper version:

```txt
torch>=1.13.0
transformers>=4.25.0
gradio>=3.40.0
```

### ❌ App won't load or takes very long

**Solutions:**
1. Check Logs tab for errors
2. Simplify your Gradio interface
3. Use smaller model or cached version
4. Enable CPU-only mode

### ❌ Git push fails

**Solution:** Use your HF token for authentication:

```bash
# Create token at https://huggingface.co/settings/tokens
# When prompted for password, paste your token (not your account password)

# Or set git credentials:
git config --global user.email "you@example.com"
git config --global user.name "Your Name"
git push  # Will prompt for token
```

---

## File Preparation Template

Use this to prepare your deployment:

```bash
#!/bin/bash
# prep.sh - Prepare files for HF Spaces

SPACE_DIR="YOUR_SPACE_NAME"
mkdir -p "$SPACE_DIR/src/core"

# Copy and rename
cp src/gui.py "$SPACE_DIR/app.py"
cp src/core/infer.py "$SPACE_DIR/src/core/"
cp src/core/io_utils.py "$SPACE_DIR/src/core/"
cp src/core/rss.py "$SPACE_DIR/src/core/"
cp requirements.txt "$SPACE_DIR/"
cp README.md "$SPACE_DIR/"

# Create init files
touch "$SPACE_DIR/src/__init__.py"
touch "$SPACE_DIR/src/core/__init__.py"

# Fix imports
sed -i 's/from src\.core\./from core\./g' "$SPACE_DIR/app.py"

echo "✅ Files prepared in $SPACE_DIR/"
```

---

## Environment Variables (Advanced)

To set environment variables in your Space:

1. Go to Space **Settings**
2. Find **"Secrets"** or **"Variables"** section
3. Add variables like:
   - `DEVICE=cpu`
   - `BATCH_SIZE=32`
   - `LOG_LEVEL=INFO`

Then use in app.py:
```python
import os
device = os.getenv("DEVICE", "cpu")
```

---

## Persistent Storage (Advanced)

If you need persistent storage (database, cache):

1. Go to Space **Settings**
2. Enable **"Persistent storage"**
3. Use `/tmp` or mounted directory for files
4. Note: Resets between Space restarts by default

---

## Performance Tips

1. **Reduce startup time:** Pre-load models
2. **Reduce model size:** Use quantized models
3. **Cache results:** Store predictions temporarily
4. **Optimize code:** Remove unnecessary operations

---

## Next Steps After Deployment

✅ **Space is live!**

Now you can:
- Share the URL with users
- Monitor usage in Logs tab
- Update code by pushing new commits
- Scale up if needed (upgrade Space)

---

## References

- [HF Spaces Documentation](https://huggingface.co/docs/hub/spaces)
- [Full Deployment Guide](HF_SPACES_DEPLOYMENT.md)
- [Gradio Docs](https://gradio.app/)

---

## Questions?

Check the full deployment guide: [HF_SPACES_DEPLOYMENT.md](HF_SPACES_DEPLOYMENT.md)

---

**Ready? Let's deploy! 🚀**
