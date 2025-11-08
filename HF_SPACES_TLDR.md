# HF Spaces Deployment - TL;DR

**Everything you need to deploy to Hugging Face Spaces RIGHT NOW**

---

## The Absolute Fastest Way (5 minutes)

```bash
# 1. Clone your HF Space
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME

# 2. Copy files from your project
cp ../financial-news-classifier/src/gui.py app.py
cp ../financial-news-classifier/src/core . -r
cp ../financial-news-classifier/requirements.txt .
cp ../financial-news-classifier/README.md .

# 3. Create __init__.py files
touch src/__init__.py src/core/__init__.py

# 4. Fix imports (remove src. prefix)
sed -i 's/from src\.core\./from core\./g' app.py

# 5. Push to HF
git add .
git commit -m "Deploy Financial News Classifier"
git push

# Done! Wait 2-5 minutes, then visit your Space URL
```

---

## Step-by-Step Checklist

- [ ] Space created on huggingface.co
- [ ] Know your HF username and space name
- [ ] `app.py` exists in Space root (renamed from gui.py)
- [ ] `requirements.txt` exists with all dependencies
- [ ] `core/` directory exists with infer.py, io_utils.py, rss.py
- [ ] All imports changed from `from src.core` to `from core`
- [ ] Files committed and pushed to HF
- [ ] Waiting for build (check Logs tab)
- [ ] Space is live at https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

---

## Directory Structure (MUST be exactly like this)

```
YOUR_SPACE_NAME/
├── app.py
├── requirements.txt
├── README.md
└── core/
    ├── __init__.py
    ├── infer.py
    ├── io_utils.py
    └── rss.py
```

---

## The Critical Import Fix

This is the #1 issue. Your `app.py` must have:

```python
# ✅ CORRECT
from core.infer import predict
from core.rss import fetch_rss
from core.io_utils import load_file

# ❌ WRONG (will fail)
from src.core.infer import predict
from src.core.rss import fetch_rss
from src.core.io_utils import load_file
```

**Fix entire file:**
```bash
sed -i 's/from src\.core\./from core\./g' app.py
```

---

## Minimal requirements.txt

```txt
torch>=1.13.0
transformers>=4.25.0
gradio>=3.40.0
numpy>=1.23.0
pandas>=1.5.0
requests>=2.28.0
feedparser>=6.0.0
```

---

## Verify Before Pushing

```bash
# Make sure structure is correct
ls -la
# Should show: app.py, requirements.txt, README.md, core/

# Check imports in app.py
grep "from src\." app.py
# Should show: nothing (0 results)

# Check that imports from core exist
grep "from core\." app.py
# Should show the imports

# Make sure core module files exist
ls core/
# Should show: __init__.py, infer.py, io_utils.py, rss.py
```

---

## Push to HF

```bash
# Stage all files
git add .

# Commit with message
git commit -m "Deploy Financial News Classifier to HF Spaces"

# Push (will prompt for HF token)
git push
```

When prompted for password: **use your HF token, not your password**
- Get token: https://huggingface.co/settings/tokens
- Needs "write" permission

---

## Monitor Deployment

After pushing:

1. Go to: https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
2. Click **"App"** tab → wait for "Building..." to complete
3. Click **"Logs"** tab → see build progress and any errors
4. App loads automatically when ready (usually 2-5 min)

---

## If It Fails

Check these in order:

1. **Look at Logs tab** - Read the error message
2. **Check app.py imports** - Make sure `from core.` not `from src.core.`
3. **Check file structure** - core/ must exist with __init__.py
4. **Check requirements.txt** - All packages must be valid
5. **Try simpler requirements** - Maybe torch version issue

---

## Common Problems & Fixes

| Error | Fix |
|-------|-----|
| `ModuleNotFoundError: No module named 'src'` | `sed -i 's/from src\.core\./from core\./g' app.py` |
| `FileNotFoundError: core/infer.py` | Copy core directory: `cp ../src/core . -r` |
| Build fails (timeout) | Remove heavy packages from requirements.txt |
| Model won't load | Ensure torch in requirements.txt |
| Import error for core | Make sure `src/` folder doesn't exist, only `core/` |

---

## After Deployment

**To update:**
```bash
# Make changes to files
# Then:
git add .
git commit -m "Update: describe changes"
git push
# Auto-redeploys!
```

**To share:**
- Link: https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
- Embed code available in Space settings
- Direct shareable link

---

## Full Documentation

For detailed information:
- **[HF_SPACES_DEPLOYMENT.md](HF_SPACES_DEPLOYMENT.md)** - Complete guide with all options
- **[QUICK_DEPLOY_HF.md](QUICK_DEPLOY_HF.md)** - Full quick reference
- **[HF Spaces Docs](https://huggingface.co/docs/hub/spaces)** - Official docs

---

## Success Checklist ✅

After deployment, you should see:
- [ ] Space URL is accessible
- [ ] Gradio interface loads
- [ ] Can type text and click "Classify"
- [ ] Gets sentiment result
- [ ] No error messages
- [ ] Can use all tabs (Classification, Batch, RSS)

If all above are ✅ → **Deployment successful! 🎉**

---

## One-Liner Deployment (if you know what you're doing)

```bash
git clone https://huggingface.co/spaces/YOUR_USER/YOUR_SPACE && cd YOUR_SPACE && cp ../financial-news-classifier/src/gui.py app.py && cp ../financial-news-classifier/src/core . -r && cp ../financial-news-classifier/requirements.txt . && cp ../financial-news-classifier/README.md . && touch src/__init__.py src/core/__init__.py && sed -i 's/from src\.core\./from core\./g' app.py && git add . && git commit -m "Deploy" && git push
```

---

**Need help? Check [HF_SPACES_DEPLOYMENT.md](HF_SPACES_DEPLOYMENT.md) for detailed troubleshooting.**

**Ready? Let's go! 🚀**
