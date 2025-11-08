# Deploying to Hugging Face Spaces

Complete guide to deploy Financial News Classifier to Hugging Face Spaces (Gradio).

---

## Prerequisites

✅ Hugging Face account (free at https://huggingface.co)
✅ Space created on HF website
✅ Git installed locally
✅ Your Financial News Classifier repository

---

## Step 1: Get Your Space Repository URL

1. Go to your Space on Hugging Face: https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
2. Click **"Files and versions"** tab
3. Click the blue **"Clone repository"** button
4. Copy the Git URL (looks like: `https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME`)

---

## Step 2: Clone Your HF Space Locally

```bash
# Clone the empty space repository
git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
cd YOUR_SPACE_NAME
```

---

## Step 3: Copy Your Project Files

Copy the necessary files from your project to the cloned space:

```bash
# From your financial-news-classifier directory
cd /path/to/financial-news-classifier

# Copy main files to space
cp src/gui.py ../YOUR_SPACE_NAME/app.py
cp src/core/ ../YOUR_SPACE_NAME/src/core/ -r
cp requirements.txt ../YOUR_SPACE_NAME/
cp README.md ../YOUR_SPACE_NAME/
```

---

## Step 4: Create app.py (Entry Point for Spaces)

Hugging Face Spaces looks for `app.py` at the root. The GUI file should be renamed:

```bash
cd YOUR_SPACE_NAME
mv gui.py app.py  # or copy with this name
```

**Your app.py should have this structure:**

```python
#!/usr/bin/env python3
"""Financial News Classifier - Gradio GUI"""

import gradio as gr
from src.core.infer import predict, predict_batch
from src.core.rss import fetch_rss
# ... rest of your GUI code ...

# Launch the app
if __name__ == "__main__":
    # Create and launch Gradio interface
    demo.launch()
```

---

## Step 5: Create/Update requirements.txt

Make sure all dependencies are listed:

```txt
torch>=1.13.0
transformers>=4.25.0
gradio>=3.40.0
numpy>=1.23.0
pandas>=1.5.0
requests>=2.28.0
feedparser>=6.0.0
huggingface-hub>=0.16.0
```

---

## Step 6: Create README.md for Space

```markdown
# Financial News Classifier

Sentiment classification for financial news articles using DistilBERT.

## Features

- **Real-time Classification**: Analyze sentiment of financial text
- **Batch Processing**: Process multiple articles at once
- **RSS Integration**: Monitor news feeds for sentiment
- **Three Classes**: Bullish, Bearish, Neutral

## Usage

1. Enter or paste financial text
2. Click "Classify"
3. View sentiment and confidence scores

## Model

Based on DistilBERT fine-tuned on FinancialPhraseBank

## About

For more information: https://github.com/TADSTech/financial-news-classifier
```

---

## Step 7: Create .gitignore

```
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
```

---

## Step 8: Optional - Create Dockerfile (for more control)

If you need custom dependencies:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=7860
ENV GRADIO_SHARE=False

# Run app
CMD ["python", "app.py"]
```

---

## Step 9: Create README.md for the Space

Create a file structure like this:

```
YOUR_SPACE_NAME/
├── app.py                    # Main Gradio app (from gui.py)
├── requirements.txt          # Python dependencies
├── README.md                 # Space description
├── .gitignore               # Git ignore patterns
├── Dockerfile               # (Optional) for custom setup
└── src/
    ├── __init__.py
    └── core/
        ├── __init__.py
        ├── infer.py         # Model inference
        ├── io_utils.py      # File I/O
        └── rss.py           # RSS processing
```

---

## Step 10: Push to HF Spaces

```bash
cd YOUR_SPACE_NAME

# Stage all files
git add .

# Commit
git commit -m "Initial deployment of Financial News Classifier"

# Push to Hugging Face
git push
```

**Git credentials:**
- If prompted, use your HF token (from https://huggingface.co/settings/tokens)
- Create a token with **write** permissions

---

## Verification

After pushing:

1. Go to your Space URL: https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
2. Click **"App"** tab - wait 2-5 minutes for deployment
3. The app should load and be accessible

**Check logs:**
- Click **"Logs"** tab to see deployment progress
- If there are errors, they'll appear here

---

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution:** Update imports in app.py:

```python
# Old (doesn't work on Spaces)
from src.core.infer import predict

# New (works on Spaces)
from core.infer import predict
```

Change your import paths to be relative or adjust the structure.

### Issue: "Space is taking too long to build"

**Solutions:**
1. Check **Logs** tab for errors
2. Reduce model size (use quantized version)
3. Simplify requirements.txt - remove unnecessary packages
4. Consider using CPU-only version

### Issue: "CUDA/GPU not available"

**Solution:** Use CPU-only Torch version in requirements.txt:

```txt
torch==2.0.1  # CPU version
# Don't specify CUDA index URL
```

Or specify explicitly:

```txt
torch==2.0.1 --index-url https://download.pytorch.org/whl/cpu
```

### Issue: "Model downloads are too slow"

**Solutions:**
1. Cache the model in Spaces:
   - Add to app.py startup:
   ```python
   from transformers import AutoModel, AutoTokenizer
   model = AutoModel.from_pretrained("TADSTech/financial-news-classifier")
   ```

2. Use smaller model:
   - Quantize with ONNX
   - Use distilled version

3. Pre-download model:
   - Add `setup.py` script that downloads on deploy

### Issue: "Out of memory during build"

**Solution:** Reduce dependencies or use smaller models:

```python
# In app.py
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
```

### Issue: "Import errors for custom modules"

**Solution:** Make sure file structure matches imports:

```python
# If app.py is in root, and core/ is in root
from core.infer import predict  ✅

# Not this:
from src.core.infer import predict  ❌
```

---

## Advanced Setup

### Option 1: Using setup.py for Custom Installation

Create `setup.py`:

```python
from setuptools import setup, find_packages

setup(
    name="financial-classifier",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "torch>=1.13.0",
        "transformers>=4.25.0",
        "gradio>=3.40.0",
    ],
)
```

Then in requirements.txt:
```
-e .
```

### Option 2: Using Secrets for Private Models

If your model is private, add to Spaces **Settings → Secrets**:

```
HF_TOKEN=hf_your_token_here
```

Then access in app.py:

```python
import os
from huggingface_hub import login

hf_token = os.getenv("HF_TOKEN")
if hf_token:
    login(token=hf_token)
```

### Option 3: Environment Variables

In Spaces **Settings → Variables**, set:

```
DEVICE=cpu
BATCH_SIZE=32
MODEL_NAME=TADSTech/financial-news-classifier
```

Access in app.py:

```python
import os

device = os.getenv("DEVICE", "cpu")
batch_size = int(os.getenv("BATCH_SIZE", "32"))
model_name = os.getenv("MODEL_NAME", "TADSTech/financial-news-classifier")
```

---

## File Structure for HF Spaces

**Minimum structure:**

```
your-space/
├── app.py              # Required! Entry point
├── requirements.txt    # Required! Dependencies
└── README.md          # Required! Space description
```

**Recommended structure:**

```
your-space/
├── app.py              # Main Gradio interface
├── requirements.txt    # Python packages
├── README.md          # Space description
├── Dockerfile         # Optional: custom setup
├── .gitignore         # Git ignore
├── .gitattributes     # Git LFS (if needed)
├── LICENSE            # License file
└── core/              # Your modules
    ├── __init__.py
    ├── infer.py       # Model inference
    ├── io_utils.py    # File operations
    └── rss.py         # RSS feeds
```

---

## Performance Tips

### Reduce Startup Time

```python
# In app.py - load model once
from core.infer import ModelLoader

# Global - loads once at startup
loader = ModelLoader()
model = loader.load_model()

def classify(text):
    # Reuse loaded model
    result = predict(text)
    return result
```

### Reduce Model Size

```python
# Use ONNX for faster inference
from optimum.onnxruntime import ORTModelForSequenceClassification

model = ORTModelForSequenceClassification.from_pretrained(
    "TADSTech/financial-news-classifier"
)
```

### Optimize Requirements

Remove unnecessary packages:

```txt
# ❌ Too heavy
torch
transformers
gradio
pandas
numpy
requests
feedparser
scikit-learn    # Not needed
matplotlib      # Not needed
jupyter         # Not needed

# ✅ Minimal
torch
transformers
gradio>=4.0
numpy
requests
feedparser
```

---

## Updating Your Space

To update your Space after making changes:

```bash
cd YOUR_SPACE_NAME

# Make changes to files

# Commit changes
git add .
git commit -m "Update classifier model"

# Push to trigger rebuild
git push

# Space will auto-rebuild
```

---

## Custom Domain (Optional)

To add a custom domain:

1. Go to Space **Settings**
2. Look for **"Space settings"** → **"Persistent storage"** or **"Custom domain"**
3. Add your domain (requires DNS configuration)

---

## Monitoring

**Check logs:**
- Click **"Logs"** tab in Space
- See real-time output and errors

**View metrics:**
- Click **"Metrics"** tab
- See visits, errors, uptime

---

## Common File Paths for Spaces

When deploying to Spaces, remember:

```python
# Spaces root = /home/user/app/

# So if you have:
app.py                 # /home/user/app/app.py
src/core/infer.py      # /home/user/app/src/core/infer.py

# Imports should be:
from core.infer import predict    # ✅ Works

# Not:
from src.core.infer import predict  # ❌ Fails
```

---

## Quick Deployment Checklist

- [ ] Space created on HF website
- [ ] Space repository cloned locally
- [ ] Project files copied to Space directory
- [ ] gui.py renamed to app.py
- [ ] Import paths updated (remove `src.`)
- [ ] requirements.txt present and complete
- [ ] README.md written for Space
- [ ] .gitignore created
- [ ] All files committed with git
- [ ] Pushed to HF repository
- [ ] Space builds successfully (check Logs)
- [ ] App loads in browser

---

## Example Complete app.py

```python
#!/usr/bin/env python3
"""Financial News Classifier - Gradio GUI for HF Spaces"""

import gradio as gr
import pandas as pd
import logging
from typing import Tuple

# Fixed imports for HF Spaces
from core.infer import predict, predict_batch
from core.rss import fetch_rss
from core.io_utils import load_file, save_results

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

SENTIMENT_COLORS = {
    "Bullish": "#10b981",
    "Bearish": "#ef4444",
    "Neutral": "#94a3b8"
}

def classify_single_text(text: str) -> str:
    """Classify single text"""
    if not text.strip():
        return "Please enter text to classify."
    
    try:
        result = predict(text)
        sentiment = result['sentiment']
        confidence = result['confidence']
        
        output = f"""
**Sentiment:** {sentiment}
**Confidence:** {confidence:.2%}
"""
        return output
    except Exception as e:
        return f"Error: {str(e)}"

def classify_batch_file(file_obj) -> Tuple[str, str]:
    """Batch classify from file"""
    if file_obj is None:
        return "Please upload a file", ""
    
    try:
        df = pd.read_csv(file_obj.name)
        texts = df.iloc[:, 0].tolist()
        results = predict_batch(texts)
        
        output_df = pd.DataFrame({
            'text': texts,
            'sentiment': [r['sentiment'] for r in results],
            'confidence': [r['confidence'] for r in results]
        })
        
        csv_output = output_df.to_csv(index=False)
        return "Processing complete!", csv_output
    except Exception as e:
        return f"Error: {str(e)}", ""

def classify_rss_feed(url: str, max_entries: int = 10) -> str:
    """Classify RSS feed"""
    try:
        articles = fetch_rss(url, max_entries=max_entries)
        results = []
        
        for article in articles:
            result = predict(article['title'])
            results.append({
                'title': article['title'][:50],
                'sentiment': result['sentiment'],
                'confidence': result['confidence']
            })
        
        output_df = pd.DataFrame(results)
        return output_df.to_markdown(index=False)
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# Financial News Classifier")
    gr.Markdown("Classify financial news sentiment using DistilBERT")
    
    with gr.Tab("Classification"):
        text_input = gr.Textbox(label="Financial Text", lines=3)
        classify_btn = gr.Button("Classify")
        output_text = gr.Markdown()
        
        classify_btn.click(
            classify_single_text,
            inputs=text_input,
            outputs=output_text
        )
    
    with gr.Tab("Batch Processing"):
        file_input = gr.File(label="Upload CSV", file_types=[".csv"])
        batch_btn = gr.Button("Process File")
        batch_status = gr.Textbox(label="Status")
        csv_output = gr.Textbox(label="Results (CSV)")
        
        batch_btn.click(
            classify_batch_file,
            inputs=file_input,
            outputs=[batch_status, csv_output]
        )
    
    with gr.Tab("RSS Analysis"):
        rss_url = gr.Textbox(label="RSS Feed URL")
        rss_entries = gr.Slider(1, 50, 10, label="Max Entries")
        rss_btn = gr.Button("Analyze Feed")
        rss_output = gr.Markdown()
        
        rss_btn.click(
            classify_rss_feed,
            inputs=[rss_url, rss_entries],
            outputs=rss_output
        )
    
    with gr.Tab("About"):
        gr.Markdown("""
## About This Model

**Model:** DistilBERT (Financial)
**Task:** Sentiment Classification
**Classes:** Bullish, Bearish, Neutral

**Performance:**
- Accuracy: 87.5%
- F1-Score: 0.86
- Speed: 50-200 texts/second

**Model Card:** [View on HF](https://huggingface.co/TADSTech/financial-news-classifier)

**Repository:** [GitHub](https://github.com/TADSTech/financial-news-classifier)
""")

if __name__ == "__main__":
    demo.launch()
```

---

## After Deployment

Once deployed:

1. **Share your Space**: Copy Space URL and share
2. **Monitor usage**: Check Logs and Metrics tabs
3. **Update as needed**: Push new changes to auto-redeploy
4. **Manage costs**: Free tier has limitations; upgrade if needed

---

## Useful Resources

- [Hugging Face Spaces Docs](https://huggingface.co/docs/hub/spaces)
- [Gradio Documentation](https://gradio.app/)
- [HF Space Examples](https://huggingface.co/spaces)
- [Git Guide](https://git-scm.com/doc)

---

## Support

If deployment fails:

1. Check **Logs** tab for error messages
2. Verify import paths match your file structure
3. Ensure all files are committed and pushed
4. Check requirements.txt for syntax errors
5. Try reducing model complexity
6. Post to [HF Forum](https://discuss.huggingface.co/) if stuck

---

**Happy deploying! 🚀**
