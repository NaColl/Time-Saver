"""Main content generator orchestrating all platform-specific generation."""

import json
import re
from datetime import datetime, timedelta
from typing import Optional
from zoneinfo import ZoneInfo

import httpx

from ..config import Settings
from ..models.article import Article, ArticleAnalysis
from ..models.social_post import (
    SocialPost,
    ContentWeek,
    Platform,
    PostType,
)
from ..prompts.base_prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT
from ..prompts.linkedin_prompts import LINKEDIN_PROMPTS, LINKEDIN_POST_SCHEDULE
from ..prompts.twitter_prompts import TWITTER_PROMPTS, TWITTER_POST_SCHEDULE
from ..prompts.notes_prompts import NOTES_PROMPTS


class ContentGenerator:
    """Generates social media content from articles using Gemini or Claude."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.tz = ZoneInfo(settings.timezone)
        self.api_provider = settings.api_provider

        # Gemini REST API endpoint
        self.gemini_url = f"https://generativelanguage.googleapis.com/v1beta/models/{settings.gemini_model}:generateContent"
        self.gemini_api_key = settings.gemini_api_key

        # Anthropic client (lazy loaded)
        self._anthropic_client = None

    @property
    def anthropic_client(self):
        """Lazy load Anthropic client."""
        if self._anthropic_client is None:
            import anthropic
            self._anthropic_client = anthropic.Anthropic(api_key=self.settings.anthropic_api_key)
        return self._anthropic_client

    def generate_week(self, article: Article) -> ContentWeek:
        """Generate a full week of content for all platforms."""
        # First, analyze the article
        article.analysis = self._analyze_article(article)

        # Generate posts for each platform
        linkedin_posts = self._generate_linkedin_posts(article)
        twitter_posts = self._generate_twitter_posts(article)
        notes_posts = self._generate_notes_posts(article)

        return ContentWeek(
            source_article_title=article.title,
            source_article_url=article.url,
            source_substack=article.source_substack,
            linkedin_posts=linkedin_posts,
            twitter_posts=twitter_posts,
            notes_posts=notes_posts,
        )

    def _analyze_article(self, article: Article) -> ArticleAnalysis:
        """Analyze article to extract key elements for content generation."""
        prompt = ANALYSIS_PROMPT.format(
            title=article.title,
            source=article.source_substack,
            category=article.category,
            content=article.content[:15000],  # Limit content length
        )

        response_text = self._call_api(prompt)

        # Extract JSON from response (handle potential markdown wrapping)
        json_match = re.search(r'\{[\s\S]*\}', response_text)
        if json_match:
            try:
                data = json.loads(json_match.group())
                return ArticleAnalysis(**data)
            except (json.JSONDecodeError, ValueError):
                pass

        # Fallback to basic analysis
        return ArticleAnalysis(
            main_thesis=article.title,
            key_points=[article.title],
        )

    def _generate_linkedin_posts(self, article: Article) -> list[SocialPost]:
        """Generate 7 LinkedIn posts from the article."""
        posts = []
        analysis = article.analysis

        for schedule in LINKEDIN_POST_SCHEDULE:
            day = schedule["day"]
            post_type = schedule["type"]

            # Get the prompt template
            prompt_template = LINKEDIN_PROMPTS.get(post_type)
            if not prompt_template:
                continue

            # Build the prompt with article data
            prompt = prompt_template.format(
                title=article.title,
                url=article.url,
                main_thesis=analysis.main_thesis if analysis else article.title,
                key_points="\n".join(f"- {p}" for p in (analysis.key_points if analysis else [])),
                statistics="\n".join(f"- {s}" for s in (analysis.statistics if analysis else [])),
                quotes="\n".join(f'- "{q}"' for q in (analysis.quotes if analysis else [])),
                story_hooks="\n".join(f"- {h}" for h in (analysis.story_hooks if analysis else [])),
                contrarian_angles="\n".join(f"- {c}" for c in (analysis.contrarian_angles if analysis else [])),
                actionable_takeaways="\n".join(f"- {t}" for t in (analysis.actionable_takeaways if analysis else [])),
            )

            # Generate content
            content = self._generate_content(prompt)

            # Calculate scheduled date/time
            scheduled_date = self._calculate_schedule_date(day)

            posts.append(SocialPost(
                platform=Platform.LINKEDIN,
                post_type=PostType(post_type.upper()) if post_type.upper() in PostType.__members__ else PostType.HOOK,
                content=content,
                scheduled_date=scheduled_date,
                scheduled_time=self.settings.post_time,
                day_number=day,
                source_article_url=article.url,
                source_article_title=article.title,
                hashtags=self._extract_hashtags(content),
            ))

        return posts

    def _generate_twitter_posts(self, article: Article) -> list[SocialPost]:
        """Generate 7 Twitter posts (mix of tweets and threads) from the article."""
        posts = []
        analysis = article.analysis

        for schedule in TWITTER_POST_SCHEDULE:
            day = schedule["day"]
            post_type = schedule["type"]

            # Get the prompt template
            prompt_template = TWITTER_PROMPTS.get(post_type)
            if not prompt_template:
                continue

            # Build the prompt with article data
            prompt = prompt_template.format(
                title=article.title,
                url=article.url,
                main_thesis=analysis.main_thesis if analysis else article.title,
                key_points="\n".join(f"- {p}" for p in (analysis.key_points if analysis else [])),
                statistics="\n".join(f"- {s}" for s in (analysis.statistics if analysis else [])),
                quotes="\n".join(f'- "{q}"' for q in (analysis.quotes if analysis else [])),
                story_hooks="\n".join(f"- {h}" for h in (analysis.story_hooks if analysis else [])),
                actionable_takeaways="\n".join(f"- {t}" for t in (analysis.actionable_takeaways if analysis else [])),
            )

            # Generate content
            content = self._generate_content(prompt)

            # Parse thread if applicable
            thread_tweets = None
            if post_type == "thread":
                thread_tweets = self._parse_thread(content)

            # Calculate scheduled date/time
            scheduled_date = self._calculate_schedule_date(day)

            posts.append(SocialPost(
                platform=Platform.TWITTER,
                post_type=PostType.THREAD if post_type == "thread" else PostType.TWEET,
                content=content,
                scheduled_date=scheduled_date,
                scheduled_time=self.settings.post_time,
                day_number=day,
                source_article_url=article.url,
                source_article_title=article.title,
                thread_tweets=thread_tweets,
            ))

        return posts

    def _generate_notes_posts(self, article: Article) -> list[SocialPost]:
        """Generate 7 Substack Notes from the article."""
        posts = []
        analysis = article.analysis

        for day in range(1, 8):
            prompt_template = NOTES_PROMPTS["note"]

            prompt = prompt_template.format(
                title=article.title,
                url=article.url,
                main_thesis=analysis.main_thesis if analysis else article.title,
                key_points="\n".join(f"- {p}" for p in (analysis.key_points if analysis else [])),
                quotes="\n".join(f'- "{q}"' for q in (analysis.quotes if analysis else [])),
                day_number=day,
            )

            content = self._generate_content(prompt)
            scheduled_date = self._calculate_schedule_date(day)

            posts.append(SocialPost(
                platform=Platform.NOTES,
                post_type=PostType.NOTE,
                content=content,
                scheduled_date=scheduled_date,
                scheduled_time=self.settings.post_time,
                day_number=day,
                source_article_url=article.url,
                source_article_title=article.title,
            ))

        return posts

    def _call_gemini_rest(self, prompt: str) -> str:
        """Call Gemini API using REST endpoint."""
        url = f"{self.gemini_url}?key={self.gemini_api_key}"

        payload = {
            "contents": [{
                "parts": [{
                    "text": f"{SYSTEM_PROMPT}\n\n{prompt}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 2000,
            }
        }

        with httpx.Client(timeout=60.0) as client:
            response = client.post(url, json=payload)
            response.raise_for_status()
            data = response.json()

            # Extract text from response
            if "candidates" in data and data["candidates"]:
                return data["candidates"][0]["content"]["parts"][0]["text"]
            return ""

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic/Claude API."""
        response = self.anthropic_client.messages.create(
            model=self.settings.claude_model,
            max_tokens=2000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text

    def _call_api(self, prompt: str) -> str:
        """Call the appropriate API (Gemini or Anthropic)."""
        if self.api_provider == "gemini" and self.gemini_api_key:
            return self._call_gemini_rest(prompt)
        else:
            return self._call_anthropic(prompt)

    def _generate_content(self, prompt: str) -> str:
        """Generate content using the configured API."""
        content = self._call_api(prompt)

        # Extract content between --- markers if present
        match = re.search(r'---\n([\s\S]*?)\n---', content)
        if match:
            return match.group(1).strip()

        return content.strip()

    def _calculate_schedule_date(self, day_number: int) -> datetime:
        """Calculate the scheduled date for a given day number."""
        today = datetime.now(self.tz)
        # Start from tomorrow
        scheduled = today + timedelta(days=day_number)
        # Set the time
        hour, minute = map(int, self.settings.post_time.split(":"))
        scheduled = scheduled.replace(hour=hour, minute=minute, second=0, microsecond=0)
        return scheduled

    def _extract_hashtags(self, content: str) -> list[str]:
        """Extract hashtags from content."""
        hashtags = re.findall(r'#(\w+)', content)
        return hashtags

    def _parse_thread(self, content: str) -> list[str]:
        """Parse a thread into individual tweets."""
        # Split by numbered format like "1/", "2/", etc.
        tweets = re.split(r'\n*\d+/\s*', content)
        # Remove empty strings and clean up
        tweets = [t.strip() for t in tweets if t.strip()]
        return tweets
