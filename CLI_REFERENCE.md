# CLI Reference

Complete command-line interface reference for Financial News Classifier.

---

## Overview

The CLI provides five main commands for sentiment classification:
- `classify` - Single text classification
- `batch` - Batch file processing
- `rss` - RSS feed analysis
- `gui` - Launch web interface
- `info` / `version` - System information

---

## Getting Help

Display available commands:
```bash
fnc --help
```

Get help for specific command:
```bash
fnc COMMAND --help
```

Enable verbose logging:
```bash
fnc --verbose COMMAND
```

---

## classify - Single Text Classification

Classify sentiment of a single text input.

### Syntax
```bash
fnc classify TEXT [OPTIONS]
```

### Arguments
- `TEXT` (required) - Text to classify

### Options
| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--detailed` | `-d` | Show all sentiment scores | false |
| `--device` | | Device: cpu, cuda, auto | auto |
| `--help` | | Show help message | |

### Examples

**Basic classification:**
```bash
fnc classify "Stock prices surge on positive earnings report"
```

**Show detailed scores:**
```bash
fnc classify "Market correction expected" --detailed
```

**Force GPU:**
```bash
fnc classify "Fed announces rate cut" --device cuda
```

**Force CPU:**
```bash
fnc classify "Company reports record revenue" --device cpu
```

### Output Format

**Basic output:**
```
Result
━━━━━━
Bullish
Confidence: 87.50%
```

**Detailed output:**
```
Result
━━━━━━
Bullish
Confidence: 87.50%

Sentiment Scores:
  Bullish    [████████████████░░░░] 87.50%
  Bearish    [███░░░░░░░░░░░░░░░░] 12.20%
  Neutral    [░░░░░░░░░░░░░░░░░░░░]  0.30%
```

---

## batch - Batch File Processing

Process multiple texts from a file.

### Syntax
```bash
fnc batch FILE [OPTIONS]
```

### Arguments
- `FILE` (required) - Input file path (CSV, JSON, TXT, MD)

### Options
| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--column` | `-c` | CSV column name | auto-detect |
| `--output` | `-o` | Output file path | none |
| `--format` | `-f` | Output format: csv, json, txt | csv |
| `--batch-size` | | Processing batch size | 32 |
| `--device` | | Device: cpu, cuda, auto | auto |
| `--help` | | Show help message | |

### Supported Formats

- **CSV** - Comma-separated values (auto-detects text column)
- **JSON** - JSON array or objects with text field
- **TXT** - One text per line
- **MD** - Markdown (extracts text content)

### Column Detection

Auto-detection searches for columns named:
- `text`, `content`, `title`, `headline`, `message`, `description`

### Examples

**Process CSV file:**
```bash
fnc batch data.csv
```

**Specify column:**
```bash
fnc batch articles.csv --column headlines
```

**Save results:**
```bash
fnc batch data.csv --output results.csv
```

**Save as JSON:**
```bash
fnc batch data.csv --output results.json --format json
```

**Process JSON file:**
```bash
fnc batch news.json --output results.csv
```

**Adjust batch size (faster with GPU):**
```bash
fnc batch large_file.csv --batch-size 64 --device cuda
```

**Small batch for low memory:**
```bash
fnc batch data.csv --batch-size 8 --device cpu
```

### Input File Format

**CSV:**
```csv
text,source
"Stock prices rise on earnings",Reuters
"Market correction expected",Bloomberg
```

**JSON:**
```json
[
  {"text": "Stock prices rise", "source": "Reuters"},
  {"text": "Market correction", "source": "Bloomberg"}
]
```

**TXT:**
```
Stock prices rise on earnings
Market correction expected
Fed announces rate cut
```

### Output Format

**CSV Output:**
```csv
text,sentiment,confidence
"Stock prices rise",Bullish,0.87
"Market correction",Bearish,0.92
```

**JSON Output:**
```json
[
  {
    "text": "Stock prices rise",
    "sentiment": "Bullish",
    "confidence": 0.87,
    "scores": {"Bullish": 0.87, "Bearish": 0.12, "Neutral": 0.01}
  }
]
```

---

## rss - RSS Feed Analysis

Fetch and classify headlines from RSS feeds.

### Syntax
```bash
fnc rss URL [OPTIONS]
```

### Arguments
- `URL` (required) - RSS feed URL

### Options
| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--max` | `-m` | Max headlines to fetch | 20 |
| `--output` | `-o` | Output file path | none |
| `--format` | `-f` | Output format: csv, json, txt | csv |
| `--device` | | Device: cpu, cuda, auto | auto |
| `--help` | | Show help message | |

### Examples

**Fetch and classify:**
```bash
fnc rss https://feeds.bloomberg.com/markets/news.rss
```

**Fetch 50 headlines:**
```bash
fnc rss https://feeds.cnbc.com/cnbcnewsrss.xml --max 50
```

**Save results:**
```bash
fnc rss https://example.com/rss --output headlines.csv
```

**Save as JSON:**
```bash
fnc rss https://example.com/rss --output headlines.json --format json
```

### Popular RSS Feeds

**Financial News:**
- `https://feeds.bloomberg.com/markets/news.rss` - Bloomberg Markets
- `https://feeds.cnbc.com/cnbcnewsrss.xml` - CNBC News
- `https://feeds.reuters.com/finance.rss` - Reuters Finance

**Market Data:**
- `https://feeds.finance.yahoo.com/rss/` - Yahoo Finance
- `https://feeds.bloomberg.com/stocks/rss.xml` - Bloomberg Stocks

### Output Format

**CSV Output:**
```csv
text,sentiment,confidence,source,published
"Stock surge",Bullish,0.89,Bloomberg,"2025-11-08"
```

**JSON Output:**
```json
[
  {
    "text": "Stock surge on earnings",
    "sentiment": "Bullish",
    "confidence": 0.89,
    "source": "Bloomberg",
    "published": "2025-11-08"
  }
]
```

---

## gui - Launch Web Interface

Launch the Gradio web interface.

### Syntax
```bash
fnc gui
```

### Description

Opens interactive web interface at `http://127.0.0.1:7860`

### Features

**Classification Tab**
- Classify single text
- Show detailed scores
- JSON output

**Batch Processing Tab**
- Upload and process files
- Auto-detect columns
- Export results

**RSS Analysis Tab**
- Monitor RSS feeds
- Fetch headlines
- Track publication dates

**About Tab**
- Feature documentation
- Usage tips
- Model information

### Browser Support

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge

---

## info - System Information

Display system and model information.

### Syntax
```bash
fnc info
```

### Output

```
System Information
PyTorch Version: 2.0.1
CUDA Available: Yes (NVIDIA RTX 3090)
CUDA Version: 12.1

Model Information
Model Source: Local (/path/to/finbert)
Max Length: 512 tokens
Sentiments: Bullish, Bearish, Neutral
```

---

## version - Version Information

Display version and build information.

### Syntax
```bash
fnc version
```

### Output

```
Financial News Classifier
Version: 0.1.0
Build: 2025-11-08
```

---

## Global Options

Available for all commands:

| Option | Short | Description |
|--------|-------|-------------|
| `--verbose` | `-v` | Enable debug logging |
| `--help` | | Show help message |

### Examples

**Enable verbose logging:**
```bash
fnc --verbose classify "Sample text"
fnc --verbose batch data.csv
```

---

## Device Selection

Control which processor to use:

### Option: `--device`

| Value | Description |
|-------|-------------|
| `auto` | Automatically choose (GPU if available) |
| `cpu` | Force CPU processing |
| `cuda` | Force CUDA GPU processing |

### Examples

```bash
# Auto (default, uses GPU if available)
fnc classify "Text" --device auto

# Force CPU
fnc classify "Text" --device cpu

# Force GPU
fnc classify "Text" --device cuda
```

### Performance Tips

- Use `--device cuda` for fast processing (if GPU available)
- Use `--device cpu` for compatibility
- Use `--batch-size 64+` with GPU for maximum speed

---

## Batch Size Tuning

Adjust batch size for performance/memory tradeoff:

```bash
# Faster processing (needs more memory)
fnc batch data.csv --batch-size 128

# Balanced (default)
fnc batch data.csv --batch-size 32

# Lower memory usage
fnc batch data.csv --batch-size 8
```

### Recommendations

| Scenario | Batch Size |
|----------|-----------|
| GPU + Large Memory | 64-128 |
| GPU + Limited Memory | 32-64 |
| CPU | 8-16 |
| Very Limited Memory | 4-8 |

---

## Output Formats

### CSV Format

Standard comma-separated values:
```csv
text,sentiment,confidence
"Sample text",Bullish,0.87
```

### JSON Format

Structured data with all details:
```json
[
  {
    "text": "Sample text",
    "sentiment": "Bullish",
    "confidence": 0.87,
    "scores": {
      "Bullish": 0.87,
      "Bearish": 0.12,
      "Neutral": 0.01
    }
  }
]
```

### TXT Format

One result per line:
```
Bullish (0.87)
Bearish (0.92)
Neutral (0.78)
```

---

## Error Handling

### Common Errors

**File not found:**
```
Error: File not found: data.csv
```
Solution: Check file path and permissions

**Invalid RSS feed:**
```
Error: Could not fetch valid RSS feed
```
Solution: Verify URL is accessible

**GPU not available:**
```
CUDA not available, using CPU
```
Solution: Install CUDA or use `--device cpu`

**Out of memory:**
```
Error: CUDA out of memory
```
Solution: Reduce batch size with `--batch-size 8`

---

## Tips & Tricks

### Speed Up Processing
```bash
# Use GPU with larger batch size
fnc batch data.csv --device cuda --batch-size 64
```

### Save Bandwidth
```bash
# Use local model (offline)
# Place model files in src/model/saved/finbert/
fnc classify "Text"
```

### Process in Parallel
```bash
# Run multiple CLI instances for different files
fnc batch file1.csv --output results1.csv &
fnc batch file2.csv --output results2.csv &
wait
```

### Export for Analysis
```bash
# Export results for Excel/Data analysis
fnc batch data.csv --output results.csv --format csv
```

### Monitor Live Feeds
```bash
# Check feed regularly
while true; do
  fnc rss https://example.com/rss --output latest.csv
  sleep 300  # Check every 5 minutes
done
```

---

## Scripting Examples

### Batch Process Multiple Files
```bash
#!/bin/bash
for file in *.csv; do
  echo "Processing $file..."
  fnc batch "$file" --output "results_${file}"
done
```

### Process and Filter Results
```bash
#!/bin/bash
# Get only bullish predictions
fnc batch data.csv --output results.json --format json
cat results.json | jq '.[] | select(.sentiment=="Bullish")'
```

### Monitor Multiple Feeds
```bash
#!/bin/bash
feeds=(
  "https://feeds.bloomberg.com/markets/news.rss"
  "https://feeds.cnbc.com/cnbcnewsrss.xml"
)

for feed in "${feeds[@]}"; do
  echo "Processing: $feed"
  fnc rss "$feed" --output "feed_$(date +%s).csv"
done
```

---

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (file not found, validation failed, etc.) |
| 2 | Interrupted (Ctrl+C) |

---

## Performance Benchmarks

### Single Text Classification
- **CPU:** ~500ms per text
- **GPU:** ~100ms per text

### Batch Processing (100 texts)
- **CPU:** ~50 seconds
- **GPU:** ~5 seconds

### RSS Feed Analysis (20 headlines)
- **CPU:** ~10 seconds
- **GPU:** ~2 seconds

---

## Environment Variables

Optional configuration:

```bash
# Force device
export DEVICE=cuda

# Set batch size
export BATCH_SIZE=64

# Set log level
export LOG_LEVEL=DEBUG
```

---

## Integration Examples

### With Shell Scripts
```bash
#!/bin/bash
result=$(fnc classify "Sample text")
echo "Classification result: $result"
```

### With Python
```python
import subprocess
import json

result = subprocess.run(
    ["fnc", "batch", "data.csv", "--output", "results.json", "--format", "json"],
    capture_output=True
)

with open("results.json") as f:
    data = json.load(f)
```

### With Cron (Scheduled)
```cron
# Process RSS feed every hour
0 * * * * /usr/local/bin/fnc rss https://example.com/rss --output /tmp/latest.csv
```

---

## Troubleshooting

### Command Not Found
```bash
# Reinstall package
pip install .
```

### Import Errors
```bash
# Check dependencies
pip install -r requirements.txt
```

### Slow Performance
```bash
# Enable GPU
fnc batch data.csv --device cuda

# Increase batch size
fnc batch data.csv --batch-size 64
```

### Memory Issues
```bash
# Reduce batch size
fnc batch data.csv --batch-size 8

# Use CPU
fnc batch data.csv --device cpu
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Help | `fnc --help` |
| Classify text | `fnc classify "text"` |
| Process file | `fnc batch data.csv` |
| Analyze RSS | `fnc rss https://example.com/rss` |
| Web UI | `fnc gui` |
| Info | `fnc info` |
| Version | `fnc version` |
| Verbose mode | `fnc --verbose COMMAND` |
