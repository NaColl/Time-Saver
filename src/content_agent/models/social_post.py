"""Social media post models."""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Literal, Optional
from enum import Enum


class Platform(str, Enum):
    """Supported social media platforms."""
    LINKEDIN = "linkedin"
    TWITTER = "twitter"
    NOTES = "notes"


class PostType(str, Enum):
    """Types of social media posts."""
    # LinkedIn types
    HOOK = "hook"
    STORY = "story"
    LISTICLE = "listicle"
    QUESTION = "question"
    CONTRARIAN = "contrarian"
    HOWTO = "howto"
    CTA = "cta"
    # Twitter types
    TWEET = "tweet"
    THREAD = "thread"
    # Notes types
    NOTE = "note"


# Character limits per platform
CHAR_LIMITS = {
    Platform.LINKEDIN: {"max": 3000, "recommended": 1300},
    Platform.TWITTER: {"max": 280, "thread_tweet_max": 280},
    Platform.NOTES: {"max": 5000, "recommended": 2000},
}


class SocialPost(BaseModel):
    """A generated social media post."""

    platform: Platform
    post_type: PostType
    content: str
    scheduled_date: datetime
    scheduled_time: str  # "17:00" format
    day_number: int = Field(ge=1, le=7)
    source_article_url: str
    source_article_title: str
    hashtags: list[str] = Field(default_factory=list)

    # For threads
    thread_tweets: Optional[list[str]] = None

    @property
    def character_count(self) -> int:
        """Get character count of main content."""
        return len(self.content)

    @property
    def is_within_limit(self) -> bool:
        """Check if post is within platform character limit."""
        limit = CHAR_LIMITS[self.platform]["max"]
        if self.post_type == PostType.THREAD and self.thread_tweets:
            return all(len(tweet) <= 280 for tweet in self.thread_tweets)
        return self.character_count <= limit

    @property
    def formatted_content(self) -> str:
        """Get content formatted for posting."""
        if self.post_type == PostType.THREAD and self.thread_tweets:
            return "\n\n---\n\n".join(
                f"{i+1}/ {tweet}" for i, tweet in enumerate(self.thread_tweets)
            )
        return self.content

    def to_csv_row(self) -> dict:
        """Convert to CSV row for Buffer/Typefully export."""
        return {
            "content": self.formatted_content,
            "scheduled_date": self.scheduled_date.strftime("%Y-%m-%d"),
            "scheduled_time": self.scheduled_time,
            "platform": self.platform.value,
            "post_type": self.post_type.value,
            "day": self.day_number,
        }


class ContentWeek(BaseModel):
    """A week's worth of generated content from one article."""

    source_article_title: str
    source_article_url: str
    source_substack: str
    generated_at: datetime = Field(default_factory=datetime.now)
    linkedin_posts: list[SocialPost] = Field(default_factory=list)
    twitter_posts: list[SocialPost] = Field(default_factory=list)
    notes_posts: list[SocialPost] = Field(default_factory=list)

    @property
    def all_posts(self) -> list[SocialPost]:
        """Get all posts across platforms."""
        return self.linkedin_posts + self.twitter_posts + self.notes_posts

    @property
    def total_posts(self) -> int:
        """Get total number of posts."""
        return len(self.all_posts)
