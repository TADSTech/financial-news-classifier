import pandas as pd
import json
import os
from typing import List, Dict, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def load_file(path: str, column: str = None, skip_empty: bool = True) -> List[str]:
    """
    Load text data from various file formats.
    
    Args:
        path (str): Path to the file
        column (str): For CSV, specify column name. Auto-detects if None.
        skip_empty (bool): Skip empty lines/cells
        
    Returns:
        List[str]: List of text strings
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If unsupported format or no valid data found
    """
    path = Path(path)
    
    # Validate file exists
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    if not path.is_file():
        raise ValueError(f"Path is not a file: {path}")
    
    ext = path.suffix.lower()
    texts = []
    
    try:
        if ext == ".csv":
            df = pd.read_csv(path)
            
            if df.empty:
                raise ValueError("CSV file is empty")
            
            # Auto-detect or use specified column
            if column:
                if column not in df.columns:
                    raise ValueError(f"Column '{column}' not found. Available: {list(df.columns)}")
                text_col = column
            else:
                # Try common text column names first
                common_names = ["text", "content", "title", "sentence", "message", "body"]
                text_col = None
                for name in common_names:
                    if name in df.columns:
                        text_col = name
                        break
                if not text_col:
                    text_col = df.columns[0]
            
            texts = df[text_col].astype(str).tolist()
            
        elif ext == ".json":
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Handle different JSON structures
            if isinstance(data, list):
                texts = [str(item) if isinstance(item, (str, int, float)) else str(item.get("text", item)) for item in data]
            elif isinstance(data, dict):
                # Try to find text field in dict
                if "text" in data:
                    texts = [str(data["text"])]
                elif "items" in data:
                    texts = [str(item.get("text", item)) for item in data["items"]]
                else:
                    texts = [str(v) for v in data.values()]
            else:
                raise ValueError("Invalid JSON structure")
                
        elif ext in [".txt", ".md"]:
            with open(path, "r", encoding="utf-8") as f:
                texts = f.readlines()
            texts = [line.strip() for line in texts]
            
        else:
            raise ValueError(f"Unsupported format: {ext}. Supported: CSV, JSON, TXT, MD")
        
        # Filter empty texts if requested
        if skip_empty:
            texts = [t for t in texts if t and len(t.strip()) > 0]
        
        if not texts:
            raise ValueError(f"No valid text data found in {path}")
        
        logger.info(f"Loaded {len(texts)} texts from {path}")
        return texts
        
    except Exception as e:
        logger.error(f"Error loading file {path}: {str(e)}")
        raise


def save_results(results: List[Dict], output_path: str, format: str = "csv") -> None:
    """
    Save classification results to file.
    
    Args:
        results (List[Dict]): List of result dictionaries with keys: 'text', 'sentiment', 'confidence'
        output_path (str): Path to save file
        format (str): Output format - 'csv', 'json', or 'txt'
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        if format == "csv":
            df = pd.DataFrame(results)
            df.to_csv(output_path, index=False)
            
        elif format == "json":
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
                
        elif format == "txt":
            with open(output_path, "w", encoding="utf-8") as f:
                for result in results:
                    f.write(f"Text: {result['text']}\n")
                    f.write(f"Sentiment: {result['sentiment']}\n")
                    f.write(f"Confidence: {result['confidence']:.4f}\n")
                    f.write("-" * 80 + "\n")
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        logger.info(f"Results saved to {output_path}")
        
    except Exception as e:
        logger.error(f"Error saving results to {output_path}: {str(e)}")
        raise


def validate_file(path: str) -> Tuple[bool, str]:
    """
    Validate if a file can be loaded.
    
    Returns:
        Tuple[bool, str]: (is_valid, message)
    """
    path = Path(path)
    
    if not path.exists():
        return False, f"File does not exist: {path}"
    
    if not path.is_file():
        return False, f"Path is not a file: {path}"
    
    ext = path.suffix.lower()
    if ext not in [".csv", ".json", ".txt", ".md"]:
        return False, f"Unsupported format: {ext}"
    
    if path.stat().st_size == 0:
        return False, "File is empty"
    
    return True, "File is valid"
