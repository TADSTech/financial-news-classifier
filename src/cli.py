import typer
from core.infer import predict
from core.io_utils import load_file
from core.rss import fetch_rss
import sys

app = typer.Typer(help="Financial News Classifier CLI")

@app.command()
def text(sentence: str):
    """Classify a single sentence."""
    sentiment, conf = predict(sentence)
    typer.echo(f"Sentiment: {sentiment} (confidence: {conf:.2f})")

@app.command()
def file(path: str):
    """Classify text lines from a file (CSV or TXT)."""
    texts = load_file(path)
    results = [predict(t) for t in texts]
    typer.echo(f"Processed {len(texts)} items:\n")
    for i, (s, conf) in enumerate(results):
        typer.echo(f"{i+1:02d}. {texts[i][:60]}... → {s} ({conf:.2f})")

@app.command()
def rss(url: str):
    """Fetch headlines from RSS feed and classify them."""
    headlines = fetch_rss(url)
    results = [predict(t) for t in headlines]
    typer.echo(f"Fetched {len(headlines)} headlines:\n")
    for i, (s, conf) in enumerate(results):
        typer.echo(f"{i+1:02d}. {headlines[i]} → {s} ({conf:.2f})")

@app.command()
def gui():
    """Launch simple local GUI."""
    from gui import launch_gui
    launch_gui()

def main():
    app()

if __name__ == "__main__":
    main()
