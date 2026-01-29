"""Configuration management for Content Agent."""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal


class SubstackSource:
    """Substack source configuration."""

    def __init__(self, name: str, url: str, category: str = "general"):
        self.name = name
        self.url = url
        self.rss = f"{url}/feed"
        self.category = category  # "general" or "investment"


# Default Substack sources
DEFAULT_SUBSTACKS = [
    SubstackSource(
        name="The Internet Economy",
        url="https://theinterneteconomy.xyz",
        category="general"
    ),
    SubstackSource(
        name="Automated Alpha",
        url="https://automatedalpha.substack.com",
        category="investment"
    ),
]


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # API Configuration - Support both Gemini and Anthropic
    gemini_api_key: str = Field(default="", validation_alias="GEMINI_API_KEY")
    anthropic_api_key: str = Field(default="", validation_alias="ANTHROPIC_API_KEY")

    # Model configuration
    gemini_model: str = Field(
        default="gemini-2.0-flash",
        validation_alias="GEMINI_MODEL"
    )
    claude_model: str = Field(
        default="claude-sonnet-4-20250514",
        validation_alias="CLAUDE_MODEL"
    )

    # Which API to use: "gemini" or "anthropic"
    api_provider: str = Field(default="gemini", validation_alias="API_PROVIDER")

    # Scheduling
    timezone: str = Field(default="Europe/Helsinki", validation_alias="TIMEZONE")
    post_time: str = Field(default="17:00", validation_alias="POST_TIME")

    # Content Generation
    posts_per_platform: int = 7
    platforms: list[str] = ["linkedin", "twitter", "notes"]

    # Output
    output_dir: str = Field(default="./output", validation_alias="OUTPUT_DIR")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()


def get_substacks() -> list[SubstackSource]:
    """Get configured Substack sources."""
    return DEFAULT_SUBSTACKS
