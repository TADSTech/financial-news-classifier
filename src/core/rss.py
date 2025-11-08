import feedparser
import logging
from typing import List, Dict
from datetime import datetime
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def fetch_rss(url: str, max_entries: int = None, timeout: int = 10) -> List[Dict]:
    """
    Fetch headlines from RSS feed with enhanced error handling.
    
    Args:
        url (str): RSS feed URL
        max_entries (int): Maximum number of entries to fetch. None for all.
        timeout (int): Request timeout in seconds
        
    Returns:
        List[Dict]: List of entries with keys: 'title', 'link', 'published', 'summary'
        
    Raises:
        ValueError: If URL is invalid or feed cannot be parsed
    """
    # Validate URL
    try:
        result = urlparse(url)
        if not all([result.scheme, result.netloc]):
            raise ValueError("Invalid URL format")
    except Exception as e:
        raise ValueError(f"Invalid URL: {str(e)}")
    
    try:
        # Parse RSS feed with timeout
        feed = feedparser.parse(url, timeout=timeout)
        
        # Check for parsing errors
        if feed.bozo:
            logger.warning(f"RSS feed parsing warning: {feed.bozo_exception}")
        
        if not feed.entries:
            logger.warning(f"No entries found in RSS feed: {url}")
            return []
        
        # Extract entries
        entries = []
        for i, entry in enumerate(feed.entries):
            if max_entries and i >= max_entries:
                break
            
            # Extract available fields with fallbacks
            entry_data = {
                'title': entry.get('title', 'N/A'),
                'link': entry.get('link', ''),
                'published': entry.get('published', datetime.now().isoformat()),
                'summary': entry.get('summary', ''),
                'source': feed.feed.get('title', 'Unknown Feed'),
            }
            
            # Skip entries with no title
            if entry_data['title'] and entry_data['title'] != 'N/A':
                entries.append(entry_data)
        
        logger.info(f"Fetched {len(entries)} entries from RSS feed")
        return entries
        
    except Exception as e:
        logger.error(f"Error fetching RSS feed {url}: {str(e)}")
        raise ValueError(f"Failed to fetch RSS feed: {str(e)}")


def fetch_rss_headlines(url: str, max_entries: int = None) -> List[str]:
    """
    Convenience function to get just headlines (titles) from RSS feed.
    
    Args:
        url (str): RSS feed URL
        max_entries (int): Maximum number of headlines to fetch
        
    Returns:
        List[str]: List of headline titles
    """
    entries = fetch_rss(url, max_entries=max_entries)
    return [entry['title'] for entry in entries]


def validate_rss_feed(url: str) -> bool:
    """
    Check if a URL is a valid RSS feed.
    
    Args:
        url (str): RSS feed URL
        
    Returns:
        bool: True if valid RSS feed, False otherwise
    """
    try:
        entries = fetch_rss(url, max_entries=1)
        return len(entries) > 0
    except Exception:
        return False
