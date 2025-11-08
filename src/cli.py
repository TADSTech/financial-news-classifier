#!/usr/bin/env python3
"""
Financial News Classifier CLI

Professional command-line interface for sentiment classification of financial news.
Supports single text, batch file processing, and RSS feed analysis.
"""

import typer
import logging
from typing import Optional
from pathlib import Path
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from core.infer import predict, predict_batch, set_device
from core.io_utils import load_file, save_results, validate_file
from core.rss import fetch_rss, validate_rss_feed

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Rich console for output
console = Console()

# Create Typer app
app = typer.Typer(
    help="Financial News Classifier - Sentiment analysis for financial news",
    rich_markup_mode="rich",
    no_args_is_help=True
)


@app.command()
def classify(
    text: str = typer.Argument(..., help="Text to classify"),
    detailed: bool = typer.Option(False, "--detailed", "-d", help="Show all sentiment scores"),
    device: str = typer.Option("auto", "--device", help="Device: 'cpu', 'cuda', or 'auto'")
):
    """
    Classify sentiment of a single text.

    Example:
        fnc classify "The stock market looks bullish today."
    """
    try:
        if device != "auto":
            set_device(device)
        
        result = predict(text)
        sentiment = result['sentiment']
        confidence = result['confidence']
        
        # Display result
        console.print()
        console.print(Panel(
            f"[bold]{sentiment}[/bold]\n[dim]Confidence: {confidence:.2%}[/dim]",
            title="Result",
            border_style="green" if sentiment == "Bullish" else "red" if sentiment == "Bearish" else "blue"
        ))
        
        if detailed:
            console.print("\n[bold]Sentiment Scores:[/bold]")
            for sent, score in result['scores'].items():
                bar_length = int(score * 20)
                bar = "█" * bar_length + "░" * (20 - bar_length)
                console.print(f"  {sent:10} [{bar}] {score:.2%}")
        
        console.print()
    
    except ValueError as e:
        console.print(f"\n[red]Error:[/red] {str(e)}\n")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}\n")
        logger.exception("Classification failed")
        sys.exit(1)


@app.command()
def batch(
    path: str = typer.Argument(..., help="File path (CSV, JSON, TXT, MD)"),
    column: Optional[str] = typer.Option(None, "--column", "-c", help="CSV column name"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Save results to file"),
    format: str = typer.Option("csv", "--format", "-f", help="Output format: csv, json, txt"),
    batch_size: int = typer.Option(32, "--batch-size", help="Batch size for processing"),
    device: str = typer.Option("auto", "--device", help="Device: 'cpu', 'cuda', or 'auto'")
):
    """
    Classify texts from a file.

    Supports: CSV, JSON, TXT, MD

    Example:
        fnc batch data.csv --output results.csv
        fnc batch data.csv --column headlines
    """
    try:
        file_path = Path(path)
        
        # Validate file
        is_valid, msg = validate_file(str(file_path))
        if not is_valid:
            console.print(f"\n[red]Error:[/red] {msg}\n")
            sys.exit(1)
        
        if device != "auto":
            set_device(device)
        
        # Load texts
        console.print(f"\nLoading texts from [bold]{file_path.name}[/bold]...")
        texts = load_file(str(file_path), column=column)
        console.print(f"Loaded {len(texts)} texts")
        
        # Process
        console.print(f"Processing with batch size {batch_size}...\n")
        results = predict_batch(texts, batch_size=batch_size)
        
        # Display results in table
        table = Table(title=f"Results: {len(results)} texts classified")
        table.add_column("Index", style="cyan", width=6)
        table.add_column("Text", style="white", width=50)
        table.add_column("Sentiment", style="green", width=10)
        table.add_column("Confidence", style="yellow", width=12)
        
        for i, result in enumerate(results[:20], 1):  # Show first 20
            text_preview = result['text'][:47] + "..." if len(result['text']) > 50 else result['text']
            table.add_row(
                str(i),
                text_preview,
                result['sentiment'],
                f"{result['confidence']:.2%}"
            )
        
        console.print(table)
        
        if len(results) > 20:
            console.print(f"\n[dim]Showing 20 of {len(results)} results[/dim]")
        
        # Save if requested
        if output:
            output_path = Path(output)
            save_results(results, str(output_path), format=format)
            console.print(f"\nResults saved to [bold]{output_path.name}[/bold]\n")
        else:
            console.print()
    
    except FileNotFoundError:
        console.print(f"\n[red]Error:[/red] File not found: {path}\n")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}\n")
        logger.exception("Batch processing failed")
        sys.exit(1)


@app.command()
def rss(
    url: str = typer.Argument(..., help="RSS feed URL"),
    max_entries: Optional[int] = typer.Option(20, "--max", "-m", help="Max headlines to fetch"),
    output: Optional[str] = typer.Option(None, "--output", "-o", help="Save results to file"),
    format: str = typer.Option("csv", "--format", "-f", help="Output format: csv, json, txt"),
    device: str = typer.Option("auto", "--device", help="Device: 'cpu', 'cuda', or 'auto'")
):
    """
    Analyze RSS feed headlines.

    Example:
        fnc rss https://feeds.bloomberg.com/markets/news.rss
        fnc rss https://example.com/feed.rss --max 30 --output results.csv
    """
    try:
        # Validate feed
        console.print("\nValidating RSS feed...")
        if not validate_rss_feed(url):
            console.print("[red]Error:[/red] Could not fetch valid RSS feed\n")
            sys.exit(1)
        
        console.print("Valid RSS feed found")
        
        if device != "auto":
            set_device(device)
        
        # Fetch entries
        console.print(f"Fetching up to {max_entries} headlines...")
        entries = fetch_rss(url, max_entries=max_entries)
        console.print(f"Fetched {len(entries)} headlines")
        
        # Extract and process
        headlines = [entry['title'] for entry in entries]
        console.print(f"Processing {len(headlines)} headlines...\n")
        results = predict_batch(headlines)
        
        # Add metadata
        for i, result in enumerate(results):
            result['source'] = entries[i].get('source', 'Unknown')
            result['published'] = entries[i].get('published', '')
        
        # Display results
        table = Table(title=f"RSS Analysis: {len(results)} headlines")
        table.add_column("Index", style="cyan", width=6)
        table.add_column("Headline", style="white", width=45)
        table.add_column("Sentiment", style="green", width=10)
        table.add_column("Confidence", style="yellow", width=12)
        table.add_column("Source", style="blue", width=12)
        
        for i, result in enumerate(results[:15], 1):  # Show first 15
            headline = result['text'][:42] + "..." if len(result['text']) > 45 else result['text']
            source = result['source'][:9] + "..." if len(result['source']) > 12 else result['source']
            table.add_row(
                str(i),
                headline,
                result['sentiment'],
                f"{result['confidence']:.2%}",
                source
            )
        
        console.print(table)
        
        if len(results) > 15:
            console.print(f"\n[dim]Showing 15 of {len(results)} results[/dim]")
        
        # Save if requested
        if output:
            output_path = Path(output)
            save_results(results, str(output_path), format=format)
            console.print(f"\nResults saved to [bold]{output_path.name}[/bold]\n")
        else:
            console.print()
    
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}\n")
        logger.exception("RSS processing failed")
        sys.exit(1)



@app.command()
def gui():
    """
    Launch the web GUI (Gradio).

    Opens interactive web interface in your browser.

    Example:
        fnc gui
    """
    try:
        console.print("\nLaunching GUI...\n")
        from gui import launch_gui
        launch_gui()
    except ImportError:
        console.print("[red]Error:[/red] Gradio not installed\n")
        console.print("Install with: [bold]pip install gradio[/bold]\n")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}\n")
        logger.exception("GUI launch failed")
        sys.exit(1)


@app.command()
def version():
    """Show version information."""
    console.print("\n[bold]Financial News Classifier[/bold]")
    console.print("[dim]Version: 0.1.0[/dim]")
    console.print("[dim]Build: 2025-11-08[/dim]\n")


@app.command()
def info():
    """Show system and model information."""
    try:
        import torch
        from core.infer import HF_MODEL_ID, LOCAL_MODEL_PATH, check_local_model

        console.print("\n[bold]System Information[/bold]")
        console.print(f"PyTorch Version: {torch.__version__}")
        
        if torch.cuda.is_available():
            console.print(f"CUDA Available: Yes ({torch.cuda.get_device_name(0)})")
            console.print(f"CUDA Version: {torch.version.cuda}")
        else:
            console.print("CUDA Available: No (using CPU)")
        
        console.print("\n[bold]Model Information[/bold]")
        
        if check_local_model():
            console.print(f"Model Source: [green]Local[/green] ({LOCAL_MODEL_PATH})")
        else:
            console.print(f"Model Source: [yellow]HuggingFace Hub[/yellow]")
            console.print(f"Model ID: {HF_MODEL_ID}")
        
        console.print("Max Length: 512 tokens")
        console.print("Sentiments: Bullish, Bearish, Neutral\n")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {str(e)}\n")
        sys.exit(1)


@app.callback()
def main_callback(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Financial News Classifier CLI"""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)


def main():
    """Entry point."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[dim]Interrupted by user[/dim]\n")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}\n")
        logger.exception("Unhandled exception")
        sys.exit(1)


if __name__ == "__main__":
    main()



@app.command()
def version():
    """Show version information."""
    console.print("\n[bold cyan]Financial News Classifier[/bold cyan]")
    console.print("[dim]Version: 0.1.0[/dim]")
    console.print("[dim]Build: 2025-11-08[/dim]\n")


@app.command()
def info():
    """Show system and model information."""
    try:
        import torch
        from core.infer import HF_MODEL_ID, DEVICE
        
        console.print("\n[bold cyan]System Information[/bold cyan]")
        console.print(f"[dim]Device:[/dim] {DEVICE}")
        console.print(f"[dim]PyTorch:[/dim] {torch.__version__}")
        
        if torch.cuda.is_available():
            console.print(f"[dim]CUDA Device:[/dim] {torch.cuda.get_device_name(0)}")
            console.print(f"[dim]CUDA Version:[/dim] {torch.version.cuda}")
        
        console.print(f"\n[bold cyan]Model Information[/bold cyan]")
        console.print(f"[dim]Model ID:[/dim] {HF_MODEL_ID}")
        console.print(f"[dim]Max Length:[/dim] 512 tokens")
        console.print(f"[dim]Classes:[/dim] Bullish, Bearish, Neutral\n")
        
    except Exception as e:
        console.print(f"[red]❌ Error:[/red] {str(e)}")
        sys.exit(1)


@app.callback()
def setup(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose logging")
):
    """Setup logging for all commands."""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Verbose mode enabled")


def main():
    """Main entry point."""
    try:
        app()
    except KeyboardInterrupt:
        console.print("\n[yellow]⏹️  Interrupted by user[/yellow]")
        sys.exit(0)
    except Exception as e:
        console.print(f"\n[red]❌ Unexpected Error:[/red] {str(e)}")
        logger.exception("Unhandled exception")
        sys.exit(1)


if __name__ == "__main__":
    main()
