# Financial News Classifier

Professional sentiment classification for financial news and market headlines using deep learning.

**Classify sentiment of financial text with:**
- Clean, professional CLI
- Beautiful Gradio web interface
- Batch processing (CSV, JSON, TXT, MD)
- Real-time RSS feed analysis
- GPU-accelerated inference
- Confidence scores for all predictions

---

## Requirements

- **Python 3.10+** (tested on 3.10, 3.11, 3.12, 3.13)
- **pip** package manager

Optional:
- **NVIDIA GPU** for faster inference (CUDA 11.8+)
- Internet connection for first-time model download (~500MB)

---

## Quick Start

### Installation
```bash
# Clone repository
git clone https://github.com/TADSTech/financial-news-classifier.git
cd financial-news-classifier

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install package
pip install .
```

### Basic Usage

**Classify single text:**
```bash
fnc classify "The stock market looks bullish today."
```

**Launch web GUI:**
```bash
fnc gui
```

**Process file:**
```bash
fnc batch data.csv --output results.csv
```

**Analyze RSS feed:**
```bash
fnc rss https://feeds.bloomberg.com/markets/news.rss
```

---

## Installation

### Step 1: Clone Repository
```bash
git clone https://github.com/TADSTech/financial-news-classifier.git
cd financial-news-classifier
```

### Step 2: Create Virtual Environment
```bash
python -m venv .venv
```

### Step 3: Activate Environment

**Linux / macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install .
```

Or:
```bash
pip install -r requirements.txt
```

---

## Usage

### Command Line Interface

View all commands:
```bash
fnc --help
```

#### Classify Single Text
```bash
fnc classify "Your text here"

# Show detailed sentiment scores
fnc classify "Your text here" --detailed

# Use specific device
fnc classify "Your text here" --device cuda
```

#### Batch Process Files
Process CSV, JSON, TXT, or MD files:
```bash
fnc batch data.csv

# Specify column name
fnc batch data.csv --column headlines

# Save results
fnc batch data.csv --output results.csv

# Save as JSON
fnc batch data.csv --output results.json --format json
```

#### Analyze RSS Feeds
Fetch and classify headlines from RSS feeds:
```bash
fnc rss https://feeds.bloomberg.com/markets/news.rss

# Fetch specific number of headlines
fnc rss https://example.com/rss --max 50

# Save results
fnc rss https://example.com/rss --output results.csv
```

#### Launch GUI
Open professional web interface:
```bash
fnc gui
```

Opens at `http://127.0.0.1:7860`

#### Show Information
```bash
# Version info
fnc version

# System and model info
fnc info
```

---

## GUI Features

Launch the Gradio web interface:
```bash
fnc gui
```

**Tabs:**

1. **Classification** - Single text analysis
   - Real-time sentiment detection
   - Confidence scores
   - Detailed sentiment breakdown
   - JSON output

2. **Batch Processing** - Process multiple texts
   - Upload files (CSV, JSON, TXT, MD)
   - Auto-detect text columns
   - Display results as table
   - Export to CSV

3. **RSS Analysis** - Monitor feed headlines
   - Enter RSS feed URL
   - Fetch latest headlines
   - See publication dates and sources
   - Export results

4. **About** - Documentation and tips
   - Feature overview
   - Sentiment explanations
   - Usage guidelines
   - Model information

---

## Python API

Use as a Python library:

```python
from core.infer import predict, predict_batch

# Single prediction
result = predict("Stock prices surge 5% on earnings beat")
print(result)
# {'sentiment': 'Bullish', 'confidence': 0.95, 'scores': {...}}

# Batch prediction
texts = ["Text 1", "Text 2", "Text 3"]
results = predict_batch(texts)
for result in results:
    print(f"{result['text']}: {result['sentiment']}")
```

---

## Configuration

### Environment Variables

Create `.env` file (optional):
```bash
# Device selection
DEVICE=auto  # or 'cpu', 'cuda'

# GUI settings
GUI_PORT=7860
GUI_THEME=default

# Logging
LOG_LEVEL=INFO
```

### Batch Processing

Large file processing tips:
- Adjust batch size: `--batch-size 64`
- Use GPU: `--device cuda`
- Model is cached locally after first download

---

## Model Details

- **Base:** DistilBERT (transformer-based)
- **Fine-tuned:** FinancialPhraseBank dataset
- **Classes:** Bullish, Bearish, Neutral
- **Max Input:** 512 tokens
- **Framework:** PyTorch + Transformers

### Local Model Support

For offline use, place model files at:
```
src/model/saved/finbert/
├── config.json
├── pytorch_model.bin
├── tokenizer.json
└── label_encoder.pkl
```

See `LOCAL_MODEL_SETUP.md` for details.

---

## Performance

| Metric | CPU | GPU |
|--------|-----|-----|
| Single Prediction | ~500ms | ~100ms |
| Batch (100 texts) | ~50s | ~5s |
| Model Size | ~500MB | ~500MB |

GPU times are approximate and depend on hardware.

---

## Troubleshooting

### Model Download Issues
```bash
# Set cache directory
export HF_HOME=~/.cache/huggingface
```

### CUDA/GPU Not Working
```bash
# Install PyTorch CPU-only
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### High Memory Usage
```bash
# Reduce batch size
fnc batch data.csv --batch-size 8
```

### Gradio/GUI Issues
```bash
# Reinstall Gradio
pip install --upgrade gradio
```

---

## Development

### Install in Development Mode
```bash
pip install -e .
```

### Run Tests
```bash
pytest tests/
```

### Build Package
```bash
python setup.py build
```

---

## Project Structure

```
financial-news-classifier/
├── src/
│   ├── cli.py              # CLI interface
│   ├── gui.py              # Gradio web interface
│   ├── core/
│   │   ├── infer.py        # Model inference
│   │   ├── io_utils.py     # File I/O
│   │   └── rss.py          # RSS processing
│   ├── model/
│   │   ├── train.py        # Training pipeline
│   │   ├── saved/          # Local models
│   │   └── config.py       # Training config
│   └── data/
│       └── prepare.py      # Data preprocessing
├── requirements.txt        # Dependencies
├── setup.py               # Package config
├── README.md              # This file
└── LICENSE                # MIT License
```

---

## License

MIT License - See [LICENSE](LICENSE)

---

## Support

For issues or questions:
- Open an issue on [GitHub](https://github.com/TADSTech/financial-news-classifier)
- Check [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md) for guides
- See [LOCAL_MODEL_SETUP.md](LOCAL_MODEL_SETUP.md) for offline model setup
