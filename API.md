# Python API Reference

Complete Python API reference for integrating Financial News Classifier in your applications.

---

## Overview

The Financial News Classifier provides a clean Python API for:
- Single text classification
- Batch prediction
- Custom device handling
- File I/O operations
- RSS feed processing

---

## Core Inference Module

Location: `src/core/infer.py`

### predict()

Classify sentiment of a single text.

**Signature:**
```python
def predict(text: str) -> Dict[str, Union[str, float]]
```

**Parameters:**
- `text` (str, required) - Text to classify (up to 5000 characters)

**Returns:**
- Dictionary containing:
  - `sentiment` (str) - Bullish, Bearish, or Neutral
  - `confidence` (float) - Confidence score (0-1)
  - `scores` (dict) - All class probabilities

**Raises:**
- `ValueError` - If text is empty or invalid
- `RuntimeError` - If model inference fails

**Example:**
```python
from core.infer import predict

result = predict("Stock prices surge on positive earnings")
print(result)
# Output:
# {
#   'sentiment': 'Bullish',
#   'confidence': 0.87,
#   'scores': {
#     'Bullish': 0.87,
#     'Bearish': 0.12,
#     'Neutral': 0.01
#   }
# }

print(f"Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']:.2%}")
```

---

### predict_batch()

Classify multiple texts efficiently.

**Signature:**
```python
def predict_batch(
    texts: List[str],
    batch_size: int = 32
) -> List[Dict]
```

**Parameters:**
- `texts` (List[str], required) - List of texts to classify
- `batch_size` (int, optional) - Batch size for processing (default: 32)

**Returns:**
- List of dictionaries with results (same format as `predict()`)

**Raises:**
- `ValueError` - If texts list is empty
- `RuntimeError` - If batch inference fails

**Example:**
```python
from core.infer import predict_batch

texts = [
    "Stock market hits new high",
    "Company reports losses",
    "Fed announces rate cut"
]

results = predict_batch(texts, batch_size=16)

for result in results:
    print(f"{result['text']}: {result['sentiment']} ({result['confidence']:.2%})")

# Output:
# Stock market hits new high: Bullish (89.5%)
# Company reports losses: Bearish (92.3%)
# Fed announces rate cut: Bullish (76.8%)
```

**Performance Tuning:**
```python
# Fast (uses more memory, good for GPU)
results = predict_batch(texts, batch_size=128)

# Balanced (default)
results = predict_batch(texts, batch_size=32)

# Memory-efficient (slower)
results = predict_batch(texts, batch_size=8)
```

---

### set_device()

Set the device for inference.

**Signature:**
```python
def set_device(device: str) -> None
```

**Parameters:**
- `device` (str) - Device to use: 'cpu', 'cuda', or 'auto'

**Example:**
```python
from core.infer import set_device, predict

# Use GPU
set_device('cuda')
result = predict("Sample text")

# Use CPU
set_device('cpu')
result = predict("Another sample")

# Auto-detect (default)
set_device('auto')
result = predict("Auto device")
```

---

### check_local_model()

Check if a local model is available.

**Signature:**
```python
def check_local_model() -> bool
```

**Returns:**
- `True` if local model files exist, `False` otherwise

**Example:**
```python
from core.infer import check_local_model, predict

if check_local_model():
    print("Using local model (offline)")
else:
    print("Will download model from HuggingFace Hub")

result = predict("Text")  # Model loads automatically
```

---

### ModelLoader Class

Singleton model loader for efficiency.

**Usage:**
```python
from core.infer import ModelLoader

# Get or load model
loader = ModelLoader()
model, tokenizer, label_encoder, device = loader.get_model()

# Manual load with custom device
loader.load_model(model_id="TADSTech/financial-news-classifier", device="cuda")
```

---

## File I/O Module

Location: `src/core/io_utils.py`

### load_file()

Load texts from a file.

**Signature:**
```python
def load_file(
    path: str,
    column: Optional[str] = None
) -> List[str]
```

**Parameters:**
- `path` (str, required) - File path (CSV, JSON, TXT, MD)
- `column` (str, optional) - CSV column name (auto-detected if not provided)

**Returns:**
- List of text strings

**Raises:**
- `FileNotFoundError` - If file doesn't exist
- `ValueError` - If file format is invalid

**Example:**
```python
from core.io_utils import load_file
from core.infer import predict_batch

# Load CSV with auto-detection
texts = load_file("data.csv")

# Load CSV with specific column
texts = load_file("data.csv", column="headlines")

# Load JSON
texts = load_file("news.json")

# Load TXT
texts = load_file("articles.txt")

# Process loaded texts
results = predict_batch(texts)
```

---

### save_results()

Save classification results to file.

**Signature:**
```python
def save_results(
    results: List[Dict],
    path: str,
    format: str = "csv"
) -> None
```

**Parameters:**
- `results` (List[Dict], required) - Results from predict_batch()
- `path` (str, required) - Output file path
- `format` (str, optional) - Format: 'csv', 'json', or 'txt' (default: 'csv')

**Example:**
```python
from core.infer import predict_batch
from core.io_utils import load_file, save_results

# Load and classify
texts = load_file("data.csv")
results = predict_batch(texts)

# Save in different formats
save_results(results, "output.csv", format="csv")
save_results(results, "output.json", format="json")
save_results(results, "output.txt", format="txt")
```

---

### validate_file()

Validate if a file is readable.

**Signature:**
```python
def validate_file(path: str) -> Tuple[bool, str]
```

**Parameters:**
- `path` (str, required) - File path to validate

**Returns:**
- Tuple of (is_valid: bool, message: str)

**Example:**
```python
from core.io_utils import validate_file

is_valid, msg = validate_file("data.csv")
if is_valid:
    print("File is valid")
else:
    print(f"Validation error: {msg}")
```

---

## RSS Module

Location: `src/core/rss.py`

### fetch_rss()

Fetch entries from an RSS feed.

**Signature:**
```python
def fetch_rss(
    url: str,
    max_entries: int = 50,
    timeout: int = 10
) -> List[Dict]
```

**Parameters:**
- `url` (str, required) - RSS feed URL
- `max_entries` (int, optional) - Maximum entries to fetch (default: 50)
- `timeout` (int, optional) - Request timeout in seconds (default: 10)

**Returns:**
- List of dictionaries with entries containing:
  - `title` - Headline
  - `link` - Article URL
  - `published` - Publication date
  - `source` - Feed source

**Raises:**
- `ValueError` - If URL is invalid or unreachable
- `TimeoutError` - If request times out

**Example:**
```python
from core.rss import fetch_rss
from core.infer import predict_batch

# Fetch RSS entries
url = "https://feeds.bloomberg.com/markets/news.rss"
entries = fetch_rss(url, max_entries=20)

# Extract headlines
headlines = [entry['title'] for entry in entries]

# Classify
results = predict_batch(headlines)

# Show results
for i, result in enumerate(results):
    entry = entries[i]
    print(f"{result['sentiment']}: {result['text']}")
    print(f"  Source: {entry['source']}")
    print(f"  Published: {entry['published']}\n")
```

---

### validate_rss_feed()

Validate if an RSS feed URL is valid.

**Signature:**
```python
def validate_rss_feed(url: str) -> bool
```

**Parameters:**
- `url` (str, required) - RSS feed URL

**Returns:**
- `True` if feed is valid, `False` otherwise

**Example:**
```python
from core.rss import validate_rss_feed, fetch_rss

url = "https://example.com/rss"
if validate_rss_feed(url):
    entries = fetch_rss(url)
    print(f"Feed has {len(entries)} entries")
else:
    print("Invalid RSS feed")
```

---

## Usage Examples

### Example 1: Simple Text Classification

```python
from core.infer import predict

# Classify single text
text = "Stock market rebounds after selling pressure"
result = predict(text)

print(f"Sentiment: {result['sentiment']}")
print(f"Confidence: {result['confidence']:.2%}")
```

Output:
```
Sentiment: Bullish
Confidence: 78.50%
```

---

### Example 2: Batch Processing with Progress

```python
from core.infer import predict_batch
from core.io_utils import load_file, save_results

# Load data
texts = load_file("financial_news.csv", column="headline")
print(f"Loaded {len(texts)} texts")

# Classify in batches
print("Classifying...")
results = predict_batch(texts, batch_size=32)

# Save results
save_results(results, "classified_news.csv", format="csv")
print(f"Saved {len(results)} results")

# Show summary
bullish = sum(1 for r in results if r['sentiment'] == 'Bullish')
bearish = sum(1 for r in results if r['sentiment'] == 'Bearish')
neutral = sum(1 for r in results if r['sentiment'] == 'Neutral')

print(f"Bullish: {bullish}, Bearish: {bearish}, Neutral: {neutral}")
```

---

### Example 3: RSS Feed Analysis

```python
from core.rss import fetch_rss, validate_rss_feed
from core.infer import predict_batch
from core.io_utils import save_results

# Validate and fetch RSS
url = "https://feeds.bloomberg.com/markets/news.rss"
if not validate_rss_feed(url):
    print("Invalid RSS feed")
    exit()

entries = fetch_rss(url, max_entries=30)
print(f"Fetched {len(entries)} headlines")

# Extract headlines and classify
headlines = [e['title'] for e in entries]
results = predict_batch(headlines)

# Add RSS metadata
for i, result in enumerate(results):
    result['source'] = entries[i].get('source', 'Unknown')
    result['link'] = entries[i].get('link', '')
    result['published'] = entries[i].get('published', '')

# Save and display
save_results(results, "market_analysis.json", format="json")

# Show top sentiments
for result in results[:5]:
    print(f"{result['sentiment']:8} | {result['text'][:50]:<50} | {result['confidence']:.2%}")
```

---

### Example 4: Custom Device Usage

```python
from core.infer import set_device, predict
import torch

# Check GPU availability
if torch.cuda.is_available():
    set_device('cuda')
    print(f"Using GPU: {torch.cuda.get_device_name(0)}")
else:
    set_device('cpu')
    print("Using CPU")

# Classify with selected device
result = predict("Financial text here")
print(f"Result: {result['sentiment']}")
```

---

### Example 5: Sentiment Distribution Analysis

```python
from core.infer import predict_batch
from core.io_utils import load_file
from collections import Counter

# Load and classify
texts = load_file("articles.csv")
results = predict_batch(texts)

# Analyze sentiment distribution
sentiments = [r['sentiment'] for r in results]
distribution = Counter(sentiments)

print("Sentiment Distribution:")
for sentiment, count in distribution.items():
    percentage = (count / len(results)) * 100
    print(f"  {sentiment:10}: {count:4} ({percentage:5.1f}%)")

# Find most confident predictions
top_confident = sorted(results, key=lambda x: x['confidence'], reverse=True)[:5]
print("\nMost Confident Predictions:")
for i, result in enumerate(top_confident, 1):
    print(f"{i}. {result['sentiment']:8} ({result['confidence']:.2%}): {result['text'][:60]}")
```

---

### Example 6: Error Handling

```python
from core.infer import predict
from core.io_utils import load_file, validate_file
from core.rss import fetch_rss

# Handle file loading errors
try:
    is_valid, msg = validate_file("data.csv")
    if not is_valid:
        print(f"File error: {msg}")
    else:
        texts = load_file("data.csv")
except FileNotFoundError:
    print("File not found")
except ValueError as e:
    print(f"Invalid file format: {e}")

# Handle prediction errors
try:
    result = predict("")  # Empty text
except ValueError as e:
    print(f"Input error: {e}")

try:
    result = predict("x" * 10000)  # Very long text
except RuntimeError as e:
    print(f"Processing error: {e}")

# Handle RSS errors
try:
    entries = fetch_rss("https://invalid-feed.com/rss")
except ValueError:
    print("Invalid RSS feed URL")
except TimeoutError:
    print("Feed request timed out")
```

---

### Example 7: Integration with Pandas

```python
import pandas as pd
from core.infer import predict_batch
from core.io_utils import load_file

# Load CSV into DataFrame
df = pd.read_csv("news_data.csv")

# Classify headline column
headlines = df['headline'].tolist()
results = predict_batch(headlines)

# Add results to DataFrame
df['sentiment'] = [r['sentiment'] for r in results]
df['confidence'] = [r['confidence'] for r in results]

# Analyze
print(df.groupby('sentiment').size())
print(df[df['confidence'] > 0.9].head())

# Export
df.to_csv("news_with_sentiment.csv", index=False)
```

---

## Performance Considerations

### Memory Usage

```python
# Large batch - uses more memory
results = predict_batch(large_text_list, batch_size=256)

# Small batch - uses less memory
results = predict_batch(large_text_list, batch_size=8)
```

### Speed Optimization

```python
# Fast (if GPU available)
set_device('cuda')
results = predict_batch(texts, batch_size=128)

# Standard
results = predict_batch(texts, batch_size=32)

# Slow but efficient
set_device('cpu')
results = predict_batch(texts, batch_size=8)
```

---

## Caching and Reuse

The model is cached after first load for performance:

```python
from core.infer import predict

# First call - loads model (~2-3 seconds)
result1 = predict("Text 1")

# Subsequent calls - reuse cached model (~0.1 seconds)
result2 = predict("Text 2")
result3 = predict("Text 3")
```

---

## Constants

Location: `src/core/infer.py`

```python
# Model configuration
HF_MODEL_ID = "TADSTech/financial-news-classifier"
LOCAL_MODEL_PATH = Path(...) / "model" / "saved" / "finbert"
MAX_LENGTH = 512
BATCH_SIZE = 32
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

---

## Type Hints

All functions include full type hints for IDE support:

```python
from core.infer import predict
from typing import get_type_hints

# Inspect function signature
hints = get_type_hints(predict)
print(hints)
# Output: {'text': <class 'str'>, 'return': typing.Dict[str, typing.Union[str, float]]}
```

---

## Logging

Enable detailed logging:

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("core.infer")

# Now all debug messages will be shown
from core.infer import predict
result = predict("Text")
```

---

## Exception Handling

All modules raise specific exceptions:

```python
from core.infer import predict
from core.io_utils import load_file
from core.rss import fetch_rss

try:
    # ValueError - invalid input
    result = predict("")
except ValueError as e:
    print(f"Invalid input: {e}")

try:
    # FileNotFoundError - file not found
    texts = load_file("missing.csv")
except FileNotFoundError as e:
    print(f"File missing: {e}")

try:
    # RuntimeError - processing failed
    result = predict("x" * 100000)
except RuntimeError as e:
    print(f"Processing failed: {e}")
```

---

## Complete Integration Example

```python
#!/usr/bin/env python3
"""Complete example: News analysis pipeline"""

from core.infer import predict_batch, set_device
from core.rss import fetch_rss
from core.io_utils import save_results
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)

def analyze_rss_feeds(feed_urls, output_file):
    """Analyze multiple RSS feeds and save results"""
    
    # Use GPU if available
    set_device('auto')
    
    all_results = []
    
    for url in feed_urls:
        print(f"Processing: {url}")
        try:
            # Fetch entries
            entries = fetch_rss(url, max_entries=25)
            headlines = [e['title'] for e in entries]
            
            # Classify
            results = predict_batch(headlines, batch_size=32)
            
            # Add metadata
            for i, result in enumerate(results):
                result['source'] = entries[i].get('source', 'Unknown')
                result['url'] = entries[i].get('link', '')
                result['published'] = entries[i].get('published', '')
                result['fetched_at'] = datetime.now().isoformat()
            
            all_results.extend(results)
            print(f"  Processed {len(results)} headlines")
            
        except Exception as e:
            print(f"  Error: {e}")
    
    # Save results
    save_results(all_results, output_file, format='json')
    print(f"Saved {len(all_results)} results to {output_file}")
    
    # Show summary
    bullish = sum(1 for r in all_results if r['sentiment'] == 'Bullish')
    print(f"\nSummary: {bullish}/{len(all_results)} bullish articles")

if __name__ == "__main__":
    feeds = [
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://feeds.cnbc.com/cnbcnewsrss.xml",
    ]
    analyze_rss_feeds(feeds, "market_sentiment.json")
```

---

## Related Resources

- See [CLI_REFERENCE.md](CLI_REFERENCE.md) for command-line usage
- See [README.md](README.md) for quick start
- See [LOCAL_MODEL_SETUP.md](LOCAL_MODEL_SETUP.md) for offline setup
