# Contributing Guide

Help improve Financial News Classifier! This guide covers development workflow, code standards, and contribution process.

---

## Getting Started

### Prerequisites

- Python 3.10+
- Git
- Virtual environment tool (venv or conda)

### Development Setup

```bash
# Clone repository
git clone https://github.com/TADSTech/financial-news-classifier.git
cd financial-news-classifier

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

---

## Project Structure

```
financial-news-classifier/
├── src/
│   ├── __init__.py
│   ├── cli.py                 # CLI entry point
│   ├── gui.py                 # Gradio GUI
│   ├── core/
│   │   ├── __init__.py
│   │   ├── infer.py           # Model inference
│   │   ├── io_utils.py        # File I/O
│   │   └── rss.py             # RSS processing
│   └── model/
│       ├── train.py           # Model training
│       └── saved/             # Model checkpoints
├── tests/
│   ├── __init__.py
│   ├── test_infer.py
│   ├── test_io.py
│   └── test_rss.py
├── docs/
│   ├── README.md
│   ├── API.md
│   ├── CLI_REFERENCE.md
│   ├── DEPLOYMENT.md
│   └── CONTRIBUTING.md
├── pyproject.toml
├── requirements.txt
└── setup.py
```

---

## Code Style Guide

### Python Standards (PEP 8)

Use `black` for formatting and `ruff` for linting:

```bash
# Format code
black src/ tests/

# Lint code
ruff check src/ tests/
ruff check --fix src/

# Type checking
mypy src/
```

### Pre-commit Hooks

Automatic checks on every commit. Config in `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.1.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
      - id: ruff-format

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
```

### Code Structure

```python
"""Module docstring with brief description."""

from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class ClassName:
    """Class docstring."""
    
    def __init__(self, param: str) -> None:
        """Initialize with parameter."""
        self.param = param
    
    def method_name(self, arg: int) -> str:
        """Method docstring with argument and return types."""
        return str(arg)

def function_name(
    arg1: str,
    arg2: int,
    optional_arg: Optional[str] = None
) -> dict:
    """
    Function docstring.
    
    Args:
        arg1: First argument
        arg2: Second argument
        optional_arg: Optional argument with default
    
    Returns:
        Dictionary with results
    
    Raises:
        ValueError: If argument invalid
    """
    if not arg1:
        raise ValueError("arg1 cannot be empty")
    
    return {"result": arg1, "count": arg2}
```

### Type Hints

Always use type hints:

```python
from typing import Dict, List, Optional, Tuple

def predict(text: str) -> Dict[str, float]:
    """Predict sentiment."""
    pass

def predict_batch(
    texts: List[str],
    batch_size: int = 32
) -> List[Dict[str, float]]:
    """Batch prediction."""
    pass

def load_config(path: Optional[str] = None) -> Dict:
    """Load configuration."""
    pass
```

---

## Testing

### Test Structure

Create tests in `tests/` directory:

```python
# tests/test_infer.py
import pytest
from core.infer import predict, predict_batch

class TestPredict:
    """Test prediction functions."""
    
    def test_predict_returns_dict(self):
        """Test predict returns valid dictionary."""
        result = predict("Positive text")
        assert isinstance(result, dict)
        assert "bullish" in result
        assert "bearish" in result
        assert "neutral" in result
    
    def test_predict_confidence_scores(self):
        """Test confidence scores sum to 1."""
        result = predict("Test text")
        total = sum(result.values())
        assert abs(total - 1.0) < 0.01
    
    def test_predict_batch_empty(self):
        """Test batch processing with empty list."""
        results = predict_batch([])
        assert results == []
    
    @pytest.mark.slow
    def test_predict_batch_large(self):
        """Test batch processing with large dataset."""
        texts = ["Text " + str(i) for i in range(1000)]
        results = predict_batch(texts, batch_size=32)
        assert len(results) == 1000
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_infer.py

# Run specific test
pytest tests/test_infer.py::TestPredict::test_predict_returns_dict

# Run with coverage
pytest --cov=src tests/

# Run with verbose output
pytest -v

# Run only fast tests (skip slow)
pytest -m "not slow"
```

### Test Fixtures

```python
# tests/conftest.py
import pytest

@pytest.fixture
def sample_texts():
    """Sample texts for testing."""
    return [
        "Stock prices are rising",
        "Market decline expected",
        "Neutral market sentiment"
    ]

@pytest.fixture
def sample_csv_file(tmp_path):
    """Create temporary CSV file for testing."""
    csv_path = tmp_path / "test.csv"
    csv_path.write_text("text\nBullish news\nBearish news")
    return csv_path
```

---

## Git Workflow

### Branch Naming

```
feature/feature-name      # New feature
bugfix/bug-description    # Bug fix
docs/documentation-topic  # Documentation
refactor/refactoring-task # Refactoring
```

### Commit Messages

Follow conventional commits:

```
feat: add batch processing to CLI
fix: resolve model loading timeout
docs: update API documentation
test: add unit tests for RSS module
refactor: improve error handling in inference
```

### Creating a Pull Request

1. **Create branch:**
```bash
git checkout -b feature/my-feature
```

2. **Make changes and commit:**
```bash
git add src/
git commit -m "feat: add new feature"
```

3. **Push to remote:**
```bash
git push origin feature/my-feature
```

4. **Open PR on GitHub:**
- Title: Clear description of changes
- Body: 
  - What problem does it solve?
  - How was it tested?
  - Any breaking changes?
  - Screenshots/examples if applicable

5. **Address review feedback:**
```bash
# Make requested changes
git add .
git commit -m "address review comments"
git push origin feature/my-feature
```

### PR Checklist

- [ ] Code follows style guide (black, ruff)
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No breaking changes (or documented)
- [ ] Commit messages are clear
- [ ] Branch is up to date with main

---

## Key Components to Modify

### Adding New CLI Command

1. Edit `src/cli.py`:

```python
import typer

app = typer.Typer()

@app.command()
def new_command(
    argument: str = typer.Argument(...),
    option: str = typer.Option("default", help="Option help")
) -> None:
    """New command description."""
    # Implementation
    console.print("[green]✓ Command completed[/green]")
```

2. Add tests in `tests/test_cli.py`:

```python
from typer.testing import CliRunner
from cli import app

runner = CliRunner()

def test_new_command():
    result = runner.invoke(app, ["new_command", "argument_value"])
    assert result.exit_code == 0
```

### Adding GUI Tab

1. Edit `src/gui.py`:

```python
with gr.Blocks() as demo:
    with gr.Tab("New Tab"):
        gr.Markdown("# New Feature")
        
        input_field = gr.Textbox(label="Input")
        output_field = gr.Textbox(label="Output")
        
        def process(text):
            # Processing logic
            return text.upper()
        
        button = gr.Button("Process")
        button.click(process, inputs=input_field, outputs=output_field)
```

### Extending Model Features

1. Edit `src/core/infer.py`:

```python
def predict_with_explanation(text: str) -> Dict:
    """Predict with attention scores."""
    model = ModelLoader().load_model()
    
    # Get logits and attention
    with torch.no_grad():
        outputs = model(inputs, output_attentions=True)
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "attention": attention_scores
    }
```

2. Update `src/core/io_utils.py` to export explanation data.

---

## Documentation Standards

### Function Docstrings

```python
def fetch_rss(
    url: str,
    max_entries: int = 50
) -> List[Dict[str, str]]:
    """
    Fetch RSS feed articles.
    
    Args:
        url: RSS feed URL
        max_entries: Maximum articles to fetch
    
    Returns:
        List of article dictionaries with keys:
        - title: Article title
        - summary: Article summary
        - published: Publication date
        - link: Article URL
    
    Raises:
        ValueError: If URL is invalid
        requests.RequestException: If fetch fails
    
    Example:
        >>> articles = fetch_rss("https://example.com/feed.xml")
        >>> len(articles)
        50
    """
```

### README Updates

When adding features:
1. Add to feature list
2. Add usage example
3. Update table of contents
4. Link to relevant documentation

---

## Performance Considerations

### Optimization Tips

```python
# Good: Batch processing
results = predict_batch(texts, batch_size=64)

# Bad: Individual predictions in loop
results = [predict(text) for text in texts]

# Good: Cache model
loader = ModelLoader()
model = loader.load_model()

# Bad: Reload model each time
def predict_many(texts):
    for text in texts:
        model = load_model()  # Don't do this!
        ...
```

### Memory Management

```python
# Good: Use generator for large datasets
def process_large_file(path):
    for batch in batch_generator(path, batch_size=32):
        yield predict_batch(batch)

# Bad: Load all in memory
texts = load_file(path)  # Could be huge
results = predict_batch(texts)
```

---

## Known Issues & Limitations

### Current Limitations

1. **Model Size**: DistilBERT is ~250MB, consider lighter models for edge deployment
2. **Sequence Length**: Max 512 tokens per input
3. **Memory**: Batch size limited by available RAM
4. **Performance**: CPU inference slow for large batches (use GPU if available)

### Roadmap

- [ ] Add ONNX export for faster inference
- [ ] Implement model quantization
- [ ] Add support for custom models
- [ ] Add fine-tuning interface
- [ ] Add model serving with TorchServe

---

## Debugging Tips

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Using Debugger

```python
# Add breakpoint
breakpoint()

# Or use pdb
import pdb; pdb.set_trace()
```

### Testing in REPL

```python
# Interactive testing
from src.core.infer import predict

result = predict("Test text")
print(result)
```

### Common Issues

| Issue | Solution |
|-------|----------|
| CUDA out of memory | Reduce batch size, use CPU |
| Model not found | Check path, download from Hub |
| Import errors | Install package with `pip install -e .` |
| Port already in use | Kill process or use different port |

---

## Communication

### Getting Help

- **Issues**: Use GitHub Issues for bugs
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact TADSTech for security issues
- **Chat**: Join our Discord (link in README)

### Reporting Bugs

Include:
1. Python version
2. OS and Python
3. Steps to reproduce
4. Expected vs actual behavior
5. Error traceback
6. Minimal reproducible example

### Feature Requests

Describe:
1. Use case
2. Why it's needed
3. Proposed implementation (optional)
4. Example usage

---

## Code Review Process

### For Reviewers

- Check code quality (style, types, docs)
- Verify tests pass and coverage maintained
- Test changes locally if possible
- Provide constructive feedback
- Approve when satisfied

### For Contributors

- Respond to feedback promptly
- Ask for clarification if unclear
- Update code based on feedback
- Re-request review after changes
- Gracefully handle rejection

---

## Release Process

### Version Numbering

Semantic versioning (MAJOR.MINOR.PATCH):
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

### Release Steps

1. Update version in `setup.py`
2. Update `CHANGELOG.md`
3. Create git tag
4. Push to main branch
5. Create GitHub Release
6. Upload to PyPI (automatic with CI/CD)

```bash
# Tag version
git tag v1.2.0
git push origin v1.2.0
```

---

## Environment Setup Tips

### Using Conda

```bash
conda create -n classifier python=3.10
conda activate classifier
pip install -e ".[dev]"
```

### Using pyenv

```bash
pyenv install 3.10.0
pyenv local 3.10.0
python -m venv .venv
source .venv/bin/activate
```

### Using Docker

```bash
docker run -it python:3.10 bash
pip install -e ".[dev]"
```

---

## Integration with IDEs

### VS Code Settings

Create `.vscode/settings.json`:

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.linting.pylintArgs": [
    "--max-line-length=100"
  ],
  "[python]": {
    "editor.defaultFormatter": "ms-python.python",
    "editor.formatOnSave": true
  }
}
```

### PyCharm Configuration

- Settings → Project → Python Interpreter: Select venv
- Settings → Tools → Python Integrated Tools → Default test runner: pytest
- Settings → Editor → Code Style → Python: Set to PEP 8

---

## Additional Resources

- [Python PEP 8](https://pep8.org/)
- [Black Documentation](https://black.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Type Hints Guide](https://realpython.com/python-type-checking/)

---

## Questions?

- Check existing issues/discussions
- Review documentation
- Ask in GitHub Discussions
- Open an issue with `[QUESTION]` prefix

**Thank you for contributing! 🙏**
