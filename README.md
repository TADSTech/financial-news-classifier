# 📈 Financial News Classifier

A lightweight tool to classify the sentiment of financial news using state-of-the-art NLP models. Supports CLI, GUI, and programmatic access.

**Features:**
- 🎯 Accurate sentiment classification (Positive, Negative, Neutral)
- 🖥️ Easy-to-use CLI and GUI
- 📰 RSS feed support for real-time news classification
- 🚀 Efficient inference with Hugging Face transformers
- 💾 Model caching for faster reuse

---

## Requirements

- **Python 3.13+**
- **pip** package manager

Optional:
- `tkinter` for GUI (usually included with Python)
- CUDA-compatible GPU for faster inference (optional)

---

## 🚀 Quick Start

```bash
# Install the package
pip install .

# Classify a single sentence
fnc text "The stock market looks bullish today."

# Launch the GUI
fnc gui
```

---

## 📦 Setup / Installation

### 1. Clone or copy the repository:
```bash
git clone <your-repo-url>
cd financial-news-classifier
```

### 2. Create a virtual environment (recommended):
```bash
python -m venv .venv
```

### 3. Activate the virtual environment:

**Linux / macOS:**
```bash
source .venv/bin/activate
```

**Windows:**
```bash
.venv\Scripts\activate
```

### 4. Install dependencies:

Option A - Install as a package:
```bash
pip install .
```

Option B - Install from requirements:
```bash
pip install -r requirements.txt
```

---

## Setup / Installation

1. **Clone or copy the repository:**
```bash
git clone <your-repo-url>
cd financial-news-classifier
````

2. **Create a virtual environment** (recommended):

```bash
python -m venv .venv
```

3. **Activate the virtual environment:**

* **Linux / macOS:**

```bash
source .venv/bin/activate
```

* **Windows:**

```bash
.venv\Scripts\activate
```

4. **Install dependencies**:

```bash
pip install -r requirements.txt
```

Or, if installing as a package:

```bash
pip install .
pip install -r requirements.txt
```

## 💻 Usage

### Command Line Interface (CLI)

```bash
fnc --help
```

#### Examples:

**Classify a single sentence:**
```bash
fnc text "The stock market looks bullish today."
```

**Classify text from a file** (CSV, TXT, or JSON):
```bash
fnc file path/to/file.csv
```

**Fetch and classify RSS headlines:**
```bash
fnc rss https://example.com/rss
```

**Launch GUI:**
```bash
fnc gui
```

**Show version:**
```bash
fnc --version
```

### Graphical User Interface (GUI)

Launch the GUI with:
```bash
python -m src.gui
```

Or via CLI:
```bash
fnc gui
```

The GUI provides:
- Text input field for single sentence classification
- File upload for batch processing
- Result display with confidence scores
- Export results to CSV

### Python API

```python
from src.model.infer import predict

result = predict("The stock market looks bullish today.")
print(result)  # {'sentiment': 'positive', 'confidence': 0.95}
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Model configuration
MODEL_NAME=distilbert-base-uncased-finetuned-sst-2-english
DEVICE=cpu  # or 'cuda' for GPU

# GUI settings
GUI_THEME=default
GUI_PORT=7860

# Logging
LOG_LEVEL=INFO
```

### Batch Processing

For processing large files or RSS feeds, the classifier will automatically:
- Cache models locally for faster reuse
- Process in batches to optimize memory usage
- Display progress bars

---

## 📊 Model Information

- **Base Model:** DistilBERT (or configurable via requirements)
- **Task:** Sentiment Classification
- **Output Classes:** Positive, Negative, Neutral
- **Input:** Text (sentences, paragraphs, or documents)

---

## 🛠️ Development

### Install in editable mode:
```bash
pip install -e .
```

### Run tests:
```bash
pytest tests/
```

### Build the package:
```bash
python setup.py build
```

---

## 🐛 Troubleshooting

### Model Download Issues
If the first run fails to download models:
```bash
# Set Hugging Face home
export HF_HOME=~/.cache/huggingface
```

### CUDA / GPU Issues
For CPU-only usage, install PyTorch without CUDA:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

### Memory Issues
For large files or low-memory systems:
```bash
# Set batch size via environment variable
export BATCH_SIZE=8
fnc file large_file.csv
```

### tkinter Not Found (GUI)
**Ubuntu/Debian:**
```bash
sudo apt-get install python3-tk
```

**macOS:**
```bash
brew install python-tk
```

---

## 📝 Notes

- The first run may download Hugging Face models (~500MB); these are cached locally for future runs
- All cached models are stored in `~/.cache/huggingface/`
- Virtual environments are reusable across projects after setup
- Results include confidence scores for each prediction
- Batch processing results are exported with timestamps

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

---

## 📧 Support

For issues or questions, please open an issue on GitHub or contact the maintainers.
