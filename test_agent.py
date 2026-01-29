#!/usr/bin/env python3
"""Test the content agent with sample article content."""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from content_agent.config import get_settings, get_substacks
from content_agent.models.article import Article, ArticleAnalysis
from content_agent.models.social_post import ContentWeek
from content_agent.generator import ContentGenerator
from content_agent.output import MarkdownWriter, JSONExporter, CSVExporter


# Sample article content (simulating a real Substack post)
SAMPLE_ARTICLE = Article(
    title="The 80/20 of AI Automation: Why Simple Wins",
    url="https://theinterneteconomy.xyz/p/80-20-ai-automation",
    content="""
The 80/20 of AI Automation: Why Simple Wins

After building 50+ automations for clients last year, I've learned something counterintuitive: the biggest productivity gains come from the simplest automations.

Not fancy AI agents. Not complex multi-step pipelines. Simple rules.

Here's what I mean:

The Complexity Trap

Most people approach automation wrong. They see the possibilities of AI and immediately jump to building elaborate systems. A client wanted an AI that would:
- Read all incoming emails
- Understand context from past conversations
- Draft personalized responses
- Learn from corrections over time

Six weeks and $15,000 later, they had a system that worked 60% of the time. The other 40%? It created more work than it saved.

What Actually Works

The automations that delivered 10x ROI were embarrassingly simple:

1. If email contains "invoice", forward to accounting
2. When document uploaded to shared folder, notify team on Slack
3. Every Friday at 5pm, generate weekly report from CRM data

That's it. No AI needed for most of it. Just good old-fashioned if-then logic.

The 80/20 Breakdown

From my work with 50+ companies:
- 80% of automation value comes from simple trigger-based workflows
- 15% comes from basic AI features (summarization, categorization)
- 5% comes from sophisticated AI agents

Yet most companies spend their time and budget on that 5%.

My Framework for Automation ROI

Before building any automation, ask:

1. What's the trigger? (New email, time-based, file upload, etc.)
2. What's the action? (Move, notify, create, update)
3. How often does this happen? (Daily tasks = highest ROI)
4. What's the failure mode? (If automation fails, what happens?)

If you can't answer these clearly, you're not ready to automate.

The Bottom Line

Start with what annoys you most. Automate the trigger, not the whole process. Review weekly, iterate monthly.

The future belongs to the "AI-augmented" professional - someone who knows when to use AI and when simple automation is enough.

Most of your competitors are overcomplicating this. That's your advantage.

Start simple. Ship fast. Iterate.
""",
    summary="Simple automations deliver 10x more ROI than complex AI systems. 80% of value comes from basic trigger-based workflows.",
    published_date=datetime.now(),
    source_substack="The Internet Economy",
    category="general",
)


def main():
    """Run the content generation test."""
    print("=" * 60)
    print("Content Agent Test - Sample Article")
    print("=" * 60)

    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n[ERROR] ANTHROPIC_API_KEY environment variable not set!")
        print("\nTo run this test:")
        print("  export ANTHROPIC_API_KEY='your-api-key-here'")
        print("  python test_agent.py")
        sys.exit(1)

    print(f"\nArticle: {SAMPLE_ARTICLE.title}")
    print(f"Source: {SAMPLE_ARTICLE.source_substack}")
    print(f"Words: {SAMPLE_ARTICLE.word_count}")

    # Initialize components
    settings = get_settings()
    generator = ContentGenerator(settings)
    markdown_writer = MarkdownWriter(settings.output_dir)
    json_exporter = JSONExporter(settings.output_dir)
    csv_exporter = CSVExporter(settings.output_dir)

    print("\n[1/4] Analyzing article and generating content...")
    week = generator.generate_week(SAMPLE_ARTICLE)

    print(f"[2/4] Generated {week.total_posts} posts")
    print(f"      - LinkedIn: {len(week.linkedin_posts)}")
    print(f"      - Twitter: {len(week.twitter_posts)}")
    print(f"      - Notes: {len(week.notes_posts)}")

    print("\n[3/4] Writing output files...")
    folder_path = markdown_writer.write_week(week)
    json_exporter.export_week(week, folder_path)
    csv_exporter.export_week(week, folder_path)

    print(f"\n[4/4] Done! Output saved to:")
    print(f"      {folder_path}")

    print("\n" + "=" * 60)
    print("Sample Output Preview")
    print("=" * 60)

    # Show preview of first LinkedIn post
    if week.linkedin_posts:
        post = week.linkedin_posts[0]
        print(f"\n--- LinkedIn Day 1 ({post.post_type.value}) ---")
        print(f"Scheduled: {post.scheduled_date.strftime('%A %B %d')} at {post.scheduled_time}")
        print(f"Characters: {post.character_count}")
        print("\n" + post.content[:500] + "..." if len(post.content) > 500 else post.content)

    # Show preview of first Twitter post
    if week.twitter_posts:
        post = week.twitter_posts[0]
        print(f"\n--- Twitter Day 1 ({post.post_type.value}) ---")
        print(f"Characters: {post.character_count}")
        print("\n" + post.content[:300] + "..." if len(post.content) > 300 else post.content)

    print("\n" + "=" * 60)
    print("Files created:")
    print("=" * 60)
    for f in sorted(folder_path.rglob("*")):
        if f.is_file():
            print(f"  {f.relative_to(folder_path)}")


if __name__ == "__main__":
    main()
