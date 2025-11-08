# Quick Model Setup - Reference Card

**Get offline access in 3 simple steps**

---

## TL;DR (30 seconds)

### 1. Download model zip from GitHub Releases
https://github.com/TADSTech/financial-news-classifier/releases
(Look for zipped-model.zip in assets)

### 2. Put in the folder
**src/model/saved/**

### 3. Done! Test it
fnc classify "Stock prices rising"


---

## Detailed Steps

### Step 1: Download Model (Linux/Mac)

```python
# Download from GitHub
curl -L https://github.com/TADSTech/financial-news-classifier/releases/download/v1.0.0-model/zipped-model.zip \
  -o ~/Downloads/zipped-model.zip

# Or using wget
wget https://github.com/TADSTech/financial-news-classifier/releases/download/v1.0.0-model/zipped-model.zip \
  -O ~/Downloads/zipped-model.zip
```

### Step 1: Download Model (Windows)

1. Visit: https://github.com/TADSTech/financial-news-classifier/releases
2. Find the **Model Package** release
3. Download `zipped-model.zip`
4. Save to `C:\Users\YourName\Downloads\`

### Step 2: Setup

**Script based Setup**

```bash
# Find where package is installed
python -c "import financial_news_classifier; print(financial_news_classifier.__file__)"

# Create model directory
mkdir -p /path/from/above/src/model/saved/

# Extract model
unzip ~/Downloads/zipped-model.zip -d /path/from/above/src/model/saved
```

### Step 3: Verify Installation

```bash
# Method 1: CLI
fnc classify "Stock market improving"

# Method 2: Python
python -c "
from financial_news_classifier.core.infer import predict
result = predict('Bullish market outlook')
print(f'{result[\"sentiment\"]}: {result[\"confidence\"]:.2%}')
"

# Method 3: Detailed check
python -c "
from financial_news_classifier.core.infer import check_local_model
if check_local_model():
    print('✅ Model ready!')
else:
    print('❌ Model not found')
"
```

---

---

## Troubleshooting

### "Package not installed"
```bash
pip install financial-news-classifier
```

### "File not found: zipped-model.zip"
- Check filename: `ls ~/Downloads/ | grep zipped`
- Check path: Make sure to use full path, not relative
- Re-download if needed

### "Permission denied when extracting"
```bash
# Try extracting to home directory first
unzip ~/Downloads/zipped-model.zip -d ~/my_models
```

### "Model still downloads from internet"
- Verify model directory: Run verification step above
- Check for typos in path
- Restart Python/CLI after setup

---

## Where Model Goes

Linux/Mac (virtual env):
```
.venv/lib/python3.10/site-packages/financial_news_classifier/src/model/saved/
```

Windows (virtual env):
```
.venv\Lib\site-packages\financial_news_classifier\src\model\saved\
```

System-wide (Linux/Mac):
```
/usr/local/lib/python3.10/site-packages/financial_news_classifier/src/model/saved/
```

---

## Commands to Use Offline

After setup, these work completely offline:

```bash
# Classify single text
fnc classify "Market conditions are bullish"

# Batch process CSV file
fnc batch data.csv --output results.csv

# Launch web interface
fnc gui

# Get system info
fnc info

# Get version
fnc version
```

**Note:** RSS command requires internet to fetch feeds, but the classifier itself works offline.

---

## Python API - Offline Usage

```python
from financial_news_classifier.core.infer import predict, predict_batch

# Single prediction
result = predict("Positive news for tech stocks")
print(result)  # {'sentiment': 'Bullish', 'confidence': 0.95}

# Batch predictions
texts = ["Text 1", "Text 2", "Text 3"]
results = predict_batch(texts, batch_size=32)

# File processing
from financial_news_classifier.core.io_utils import load_file, save_results

data = load_file("articles.csv")
results = predict_batch(data)
save_results(results, "output.csv")
```

---

## Verify It's Using Local Model

Add this to your code to confirm it's using the local model:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from financial_news_classifier.core.infer import predict

result = predict("Test text")

# Should see in logs: "Loading model from: /path/to/"
# NOT from HuggingFace Hub
```

---

## Quick Checks

| Check | Command |
|-------|---------|
| Package installed? | `pip show financial-news-classifier` |
| Model exists? | `fnc info` → Look for "Model: Local" |
| Python API works? | `python -c "from financial_news_classifier.core.infer import predict; print(predict('test'))"` |
| CLI works? | `fnc classify "test text"` |
| Web GUI works? | `fnc gui` |

---

## What You'll See

**With local model (offline):**
```
$ fnc info
...
Model Location: /path/to/src/model/saved/zipped
Model Source: Local
Device: CPU
...
```

**Without local model (falls back to download):**
```
$ fnc info
...
Model Location: ~/.cache/huggingface/...
Model Source: HuggingFace Hub (downloaded)
Device: CPU
...
```

---

## Next Steps After Setup

1. ✅ Verify model works (run verification commands)
2. ✅ Try classification (run example commands)
3. ✅ Read more docs if needed
4. ✅ Use offline!

---