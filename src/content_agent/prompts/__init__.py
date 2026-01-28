"""Prompt templates for content generation."""

from .base_prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT
from .linkedin_prompts import LINKEDIN_PROMPTS, LINKEDIN_POST_SCHEDULE
from .twitter_prompts import TWITTER_PROMPTS, TWITTER_POST_SCHEDULE
from .notes_prompts import NOTES_PROMPTS

__all__ = [
    "SYSTEM_PROMPT",
    "ANALYSIS_PROMPT",
    "LINKEDIN_PROMPTS",
    "LINKEDIN_POST_SCHEDULE",
    "TWITTER_PROMPTS",
    "TWITTER_POST_SCHEDULE",
    "NOTES_PROMPTS",
]
