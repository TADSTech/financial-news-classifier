import feedparser

def fetch_rss(url: str):
    feed = feedparser.parse(url)
    headlines = [entry.title for entry in feed.entries]
    return headlines
