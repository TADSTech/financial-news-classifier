#!/usr/bin/env python3
"""
Financial News Classifier - Gradio GUI

Professional web interface for sentiment classification of financial news.
Built with Gradio for clean, modern UI.
"""

import gradio as gr
import pandas as pd
import logging
from typing import Tuple, List, Dict
import json
from io import StringIO

from core.infer import predict, predict_batch, set_device
from core.rss import fetch_rss, validate_rss_feed
from core.io_utils import load_file, save_results

logger = logging.getLogger(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Color schemes for sentiment
SENTIMENT_COLORS = {
    "Bullish": "#10b981",      # Green
    "Bearish": "#ef4444",      # Red
    "Neutral": "#94a3b8"       # Slate
}


def classify_single_text(text: str, show_details: bool = False) -> Tuple[str, str]:
    """
    Classify a single text input.
    
    Returns:
        Tuple of (formatted_output, json_details)
    """
    if not text.strip():
        return "Please enter some text to classify.", "{}"
    
    try:
        result = predict(text)
        sentiment = result['sentiment']
        confidence = result['confidence']
        
        if show_details:
            # Format detailed output with all scores
            scores_text = "\n".join([
                f"**{sent}**: {score:.2%}"
                for sent, score in result['scores'].items()
            ])
            
            output = f"""
## {sentiment}

**Confidence:** {confidence:.2%}

### Sentiment Scores
{scores_text}

### Input Text
> {text[:200]}{'...' if len(text) > 200 else ''}
"""
            json_details = json.dumps(result, indent=2)
        else:
            output = f"## {sentiment}\n\n**Confidence Score:** {confidence:.2%}"
            json_details = json.dumps({
                "sentiment": sentiment,
                "confidence": confidence
            }, indent=2)
        
        return output, json_details
        
    except Exception as e:
        return f"Error: {str(e)}", "{}"


def classify_batch_file(
    file_obj,
    column_name: str = None,
    batch_size: int = 32
) -> Tuple[str, pd.DataFrame]:
    """
    Process a batch file (CSV, JSON, etc).
    
    Returns:
        Tuple of (status_message, results_dataframe)
    """
    try:
        if file_obj is None:
            return "Please upload a file", pd.DataFrame()
        
        # Load file
        file_path = file_obj.name
        texts = load_file(file_path, column=column_name)
        
        if not texts:
            return "No valid texts found in file", pd.DataFrame()
        
        # Process in batches
        results = predict_batch(texts, batch_size=batch_size)
        
        # Convert to DataFrame for display
        df = pd.DataFrame(results)
        
        # Format confidence as percentage
        df['confidence_pct'] = df['confidence'].apply(lambda x: f"{x:.2%}")
        
        status = f"Successfully processed {len(results)} texts"
        
        return status, df[['text', 'sentiment', 'confidence_pct']]
        
    except Exception as e:
        return f"Error: {str(e)}", pd.DataFrame()


def classify_rss_feed(
    url: str,
    max_entries: int = 20,
    auto_fetch: bool = True
) -> Tuple[str, pd.DataFrame]:
    """
    Fetch and classify RSS feed headlines.
    
    Returns:
        Tuple of (status_message, results_dataframe)
    """
    try:
        if not url.strip():
            return "Please enter an RSS feed URL", pd.DataFrame()
        
        # Validate feed
        if not validate_rss_feed(url):
            return "Invalid RSS feed URL", pd.DataFrame()
        
        # Fetch entries
        entries = fetch_rss(url, max_entries=max_entries)
        
        if not entries:
            return "No entries found in RSS feed", pd.DataFrame()
        
        # Extract headlines
        headlines = [entry['title'] for entry in entries]
        
        # Process headlines
        results = predict_batch(headlines, batch_size=32)
        
        # Enrich with metadata
        for i, result in enumerate(results):
            result['source'] = entries[i].get('source', 'Unknown')
            result['link'] = entries[i].get('link', '')
            result['published'] = entries[i].get('published', '')
        
        # Convert to DataFrame
        df = pd.DataFrame(results)
        df['confidence_pct'] = df['confidence'].apply(lambda x: f"{x:.2%}")
        
        source_name = entries[0].get('source', 'RSS Feed') if entries else 'RSS Feed'
        status = f"Successfully analyzed {len(results)} headlines from {source_name}"
        
        # Return relevant columns for display
        display_df = df[['text', 'sentiment', 'confidence_pct', 'source', 'published']]
        
        return status, display_df
        
    except Exception as e:
        return f"Error: {str(e)}", pd.DataFrame()


def export_results_to_csv(df: pd.DataFrame, sentiment_filter: str = "All") -> str:
    """Export results to CSV format."""
    try:
        if df.empty:
            return "No results to export"
        
        # Filter if needed
        if sentiment_filter != "All":
            df = df[df['sentiment'] == sentiment_filter]
        
        csv = df.to_csv(index=False)
        return f"Exported {len(df)} rows to CSV"
        
    except Exception as e:
        return f"Export failed: {str(e)}"


def create_gui() -> gr.Blocks:
    """
    Create the Gradio interface with multiple tabs and features.
    
    Returns:
        Gradio Blocks object
    """
    
    with gr.Blocks(
        title="Financial News Classifier",
        theme=gr.themes.Soft()
    ) as demo:
        
        # Header
        gr.Markdown(
            """
            # Financial News Classifier
            
            Sentiment classification for financial news and market headlines using deep learning.
            """
        )
        
        with gr.Tabs():
            
            # ===== TAB 1: SINGLE TEXT =====
            with gr.Tab("Classification", id="text_tab"):
                gr.Markdown("Classify a single headline or news article")
                
                with gr.Row():
                    with gr.Column(scale=2):
                        text_input = gr.Textbox(
                            label="Text Input",
                            placeholder="Enter financial news or headline...",
                            lines=4,
                            info="Paste your text here"
                        )
                        
                        with gr.Row():
                            detailed_checkbox = gr.Checkbox(
                                label="Show detailed scores",
                                value=False
                            )
                            clear_btn = gr.ClearButton(text_input)
                    
                    with gr.Column(scale=1):
                        submit_btn = gr.Button(
                            "Classify",
                            variant="primary",
                            scale=2
                        )
                
                with gr.Row():
                    with gr.Column():
                        output_markdown = gr.Markdown()
                    with gr.Column():
                        output_json = gr.Code(
                            language="json",
                            label="Output Data"
                        )
                
                # Event handlers
                submit_btn.click(
                    classify_single_text,
                    inputs=[text_input, detailed_checkbox],
                    outputs=[output_markdown, output_json]
                )
                
                text_input.submit(
                    classify_single_text,
                    inputs=[text_input, detailed_checkbox],
                    outputs=[output_markdown, output_json]
                )
                
                # Examples
                gr.Examples(
                    examples=[
                        "Stock market hits all-time high",
                        "Fed cuts interest rates by 25 basis points",
                        "Company reports record revenue",
                        "Market correction expected amid rising inflation",
                        "Earnings exceeded analyst expectations"
                    ],
                    inputs=text_input
                )
            
            # ===== TAB 2: BATCH FILE =====
            with gr.Tab("Batch Processing", id="batch_tab"):
                gr.Markdown("Process multiple texts from a file")
                gr.Markdown(
                    "Supported formats: CSV, JSON, TXT, MD\n\n"
                    "For CSV files, the app will auto-detect text columns"
                )
                
                with gr.Row():
                    with gr.Column(scale=1):
                        file_input = gr.File(
                            label="Upload File",
                            file_types=[".csv", ".json", ".txt", ".md"],
                            type="filepath"
                        )
                        
                        column_input = gr.Textbox(
                            label="Column Name (CSV only)",
                            placeholder="Leave empty for auto-detection",
                            info="Specify CSV column name containing text"
                        )
                        
                        batch_size_slider = gr.Slider(
                            minimum=8,
                            maximum=128,
                            value=32,
                            step=8,
                            label="Batch Size",
                            info="Larger value = faster but uses more memory"
                        )
                        
                        process_btn = gr.Button(
                            "Process File",
                            variant="primary",
                            scale=2
                        )
                    
                    with gr.Column(scale=2):
                        status_output = gr.Markdown()
                
                # Results table
                results_df = gr.Dataframe(
                    headers=["text", "sentiment", "confidence_pct"],
                    label="Results"
                )
                
                # Export options
                with gr.Row():
                    export_sentiment_filter = gr.Dropdown(
                        choices=["All", "Bullish", "Bearish", "Neutral"],
                        value="All",
                        label="Filter by Sentiment"
                    )
                    export_btn = gr.Button("Export as CSV")
                
                export_status = gr.Textbox(
                    label="Export Status",
                    interactive=False
                )
                
                # Event handlers
                process_btn.click(
                    classify_batch_file,
                    inputs=[file_input, column_input, batch_size_slider],
                    outputs=[status_output, results_df]
                )
                
                export_btn.click(
                    export_results_to_csv,
                    inputs=[results_df, export_sentiment_filter],
                    outputs=export_status
                )
            
            # ===== TAB 3: RSS FEED =====
            with gr.Tab("RSS Analysis", id="rss_tab"):
                gr.Markdown("Analyze RSS feed headlines")
                gr.Markdown(
                    "Enter an RSS feed URL to fetch and classify the latest headlines.\n\n"
                    "Example feeds:\n"
                    "- https://feeds.bloomberg.com/markets/news.rss\n"
                    "- https://feeds.cnbc.com/cnbcnewsrss.xml\n"
                    "- https://feeds.reuters.com/finance.rss"
                )
                
                with gr.Row():
                    with gr.Column(scale=2):
                        rss_url_input = gr.Textbox(
                            label="RSS Feed URL",
                            placeholder="https://example.com/feed.rss",
                            info="Enter the RSS feed URL"
                        )
                    
                    with gr.Column(scale=1):
                        rss_max_entries = gr.Slider(
                            minimum=5,
                            maximum=100,
                            value=20,
                            step=5,
                            label="Max Headlines"
                        )
                
                with gr.Row():
                    rss_fetch_btn = gr.Button(
                        "Fetch & Analyze",
                        variant="primary",
                        scale=1
                    )
                    rss_clear_btn = gr.ClearButton(rss_url_input, scale=1)
                
                rss_status = gr.Markdown()
                
                # Results
                rss_results_df = gr.Dataframe(
                    headers=["text", "sentiment", "confidence_pct", "source", "published"],
                    label="Headlines"
                )
                
                # Event handlers
                rss_fetch_btn.click(
                    classify_rss_feed,
                    inputs=[rss_url_input, rss_max_entries],
                    outputs=[rss_status, rss_results_df]
                )
                
                # Example feeds
                gr.Examples(
                    examples=[
                        ["https://feeds.bloomberg.com/markets/news.rss", 20],
                        ["https://feeds.cnbc.com/cnbcnewsrss.xml", 15],
                    ],
                    inputs=[rss_url_input, rss_max_entries]
                )
            
            # ===== TAB 4: ABOUT =====
            with gr.Tab("About", id="about_tab"):
                gr.Markdown(
                    """
                    ## Financial News Classifier
                    
                    Classify sentiment of financial news using state-of-the-art machine learning.
                    
                    ### Features
                    - Accurate sentiment classification with confidence scores
                    - Three sentiment classes: Bullish, Bearish, Neutral
                    - GPU-accelerated inference
                    - Batch processing for large datasets
                    - RSS feed monitoring
                    - Export results to CSV
                    
                    ### Sentiment Categories
                    
                    | Sentiment | Description |
                    |-----------|-------------|
                    | **Bullish** | Positive market outlook or favorable news |
                    | **Bearish** | Negative market outlook or unfavorable news |
                    | **Neutral** | Neutral, factual news without sentiment |
                    
                    ### Model Information
                    - **Architecture:** DistilBERT (fine-tuned)
                    - **Framework:** PyTorch + Transformers
                    - **Training Data:** FinancialPhraseBank
                    - **Input:** Text up to 512 tokens
                    - **Output:** Sentiment + Confidence score
                    
                    ### How to Use
                    
                    **Single Text:** Enter text and click Classify
                    
                    **Batch Processing:** Upload CSV/JSON file with news articles
                    
                    **RSS Monitoring:** Paste an RSS feed URL to analyze headlines
                    
                    ### Technical Details
                    - **Language:** Python 3.10+
                    - **Frontend:** Gradio
                    - **ML Framework:** PyTorch
                    - **Deployment:** Self-hosted or cloud
                    
                    ### Usage Tips
                    - Longer texts generally produce more accurate results
                    - Batch processing is significantly faster for multiple texts
                    - RSS feed analysis updates with latest headlines
                    - Detailed scores show confidence for each sentiment class
                    """
                )
    
    return demo


def launch_gui(share: bool = True, server_name: str = "127.0.0.1", server_port: int = 7860):
    """
    Launch the Gradio interface.
    
    Args:
        share (bool): Create a public link (Gradio tunnel)
        server_name (str): Server hostname
        server_port (int): Server port
    """
    demo = create_gui()
    
    demo.launch(
        share=share,
        server_name=server_name,
        server_port=server_port,
        show_error=True,
        show_api=False
    )


if __name__ == "__main__":
    launch_gui()
