"""Article data model for Substack content."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ArticleAnalysis(BaseModel):
    """AI-extracted analysis of an article."""

    main_thesis: str = Field(description="Core argument in one sentence")
    key_points: list[str] = Field(default_factory=list, description="5-7 main takeaways")
    quotes: list[str] = Field(default_factory=list, description="Notable quotable sentences")
    statistics: list[str] = Field(default_factory=list, description="Data points and numbers")
    contrarian_angles: list[str] = Field(default_factory=list, description="Challenges to conventional wisdom")
    story_hooks: list[str] = Field(default_factory=list, description="Personal anecdotes or case studies")
    actionable_takeaways: list[str] = Field(default_factory=list, description="What readers can DO")


class Article(BaseModel):
    """Represents a Substack article."""

    title: str
    url: str
    content: str  # Full article text
    summary: Optional[str] = None
    published_date: datetime
    source_substack: str
    category: str = "general"  # "general" or "investment"
    analysis: Optional[ArticleAnalysis] = None

    @property
    def slug(self) -> str:
        """Generate a URL-safe slug from the title."""
        import re
        slug = self.title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        return slug[:50].strip('-')

    @property
    def word_count(self) -> int:
        """Get approximate word count."""
        return len(self.content.split())
