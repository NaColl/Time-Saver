"""RSS fetcher for Substack articles."""

import feedparser
import httpx
from bs4 import BeautifulSoup
from datetime import datetime
from typing import Optional
import re

from ..models.article import Article
from ..config import SubstackSource


class SubstackFetcher:
    """Fetches articles from Substack RSS feeds."""

    def __init__(self, substacks: list[SubstackSource]):
        self.substacks = substacks
        self.client = httpx.Client(
            timeout=30.0,
            follow_redirects=True,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; ContentAgent/1.0)"
            }
        )

    def fetch_latest_posts(self, limit: int = 1) -> list[Article]:
        """Fetch the latest posts from all configured Substacks."""
        articles = []

        for substack in self.substacks:
            try:
                feed = feedparser.parse(substack.rss)

                for entry in feed.entries[:limit]:
                    # Get full article content
                    full_content = self._fetch_full_article(entry.link)

                    # Parse published date
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        published = datetime(*entry.published_parsed[:6])
                    else:
                        published = datetime.now()

                    article = Article(
                        title=entry.title,
                        url=entry.link,
                        content=full_content,
                        summary=entry.get("summary", ""),
                        published_date=published,
                        source_substack=substack.name,
                        category=substack.category,
                    )
                    articles.append(article)

            except Exception as e:
                print(f"Error fetching from {substack.name}: {e}")
                continue

        return articles

    def fetch_article_by_url(self, url: str) -> Optional[Article]:
        """Fetch a specific article by URL."""
        try:
            full_content = self._fetch_full_article(url)

            # Try to extract title from page
            response = self.client.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            title_tag = soup.find("h1", class_="post-title")
            title = title_tag.get_text(strip=True) if title_tag else "Untitled"

            # Determine which substack this is from
            source_name = "Unknown"
            category = "general"
            for substack in self.substacks:
                if substack.url in url:
                    source_name = substack.name
                    category = substack.category
                    break

            return Article(
                title=title,
                url=url,
                content=full_content,
                published_date=datetime.now(),
                source_substack=source_name,
                category=category,
            )

        except Exception as e:
            print(f"Error fetching article from {url}: {e}")
            return None

    def _fetch_full_article(self, url: str) -> str:
        """Fetch and extract full article text from Substack URL."""
        try:
            response = self.client.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Substack article content is in .body or .post-content class
            article_body = (
                soup.find("div", class_="body markup")
                or soup.find("div", class_="post-content")
                or soup.find("div", class_="body")
                or soup.find("article")
            )

            if article_body:
                return self._clean_article_text(article_body)

            return ""

        except Exception as e:
            print(f"Error extracting article content: {e}")
            return ""

    def _clean_article_text(self, soup_element) -> str:
        """Clean HTML and extract readable text."""
        # Remove scripts, styles, buttons, etc.
        for tag in soup_element(["script", "style", "button", "nav", "footer"]):
            tag.decompose()

        # Remove subscription CTAs and share buttons
        for div in soup_element.find_all("div", class_=re.compile(r"subscribe|share|button")):
            div.decompose()

        # Get text with proper spacing
        text = soup_element.get_text(separator="\n", strip=True)

        # Clean up excessive newlines
        text = re.sub(r'\n{3,}', '\n\n', text)

        return text.strip()

    def close(self):
        """Close the HTTP client."""
        self.client.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
