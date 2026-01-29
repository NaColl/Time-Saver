#!/usr/bin/env python3
"""Demonstrate the content agent prompts and structure."""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from content_agent.prompts.base_prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT
from content_agent.prompts.linkedin_prompts import LINKEDIN_PROMPTS, LINKEDIN_POST_SCHEDULE
from content_agent.prompts.twitter_prompts import TWITTER_PROMPTS, TWITTER_POST_SCHEDULE
from content_agent.models.article import Article, ArticleAnalysis
from content_agent.models.social_post import SocialPost, ContentWeek, Platform, PostType
from content_agent.output import MarkdownWriter, JSONExporter, CSVExporter


# Sample article
SAMPLE_ARTICLE = Article(
    title="The 80/20 of AI Automation: Why Simple Wins",
    url="https://theinterneteconomy.xyz/p/80-20-ai-automation",
    content="After building 50+ automations for clients last year, I've learned something counterintuitive: the biggest productivity gains come from the simplest automations...",
    published_date=datetime.now(),
    source_substack="The Internet Economy",
    category="general",
)

# Sample analysis (what Claude would extract)
SAMPLE_ANALYSIS = ArticleAnalysis(
    main_thesis="Simple automations deliver 10x more ROI than complex AI systems - 80% of value comes from basic trigger-based workflows.",
    key_points=[
        "80% of automation value comes from simple trigger-based workflows",
        "Most companies spend budget on sophisticated AI (5% of value) instead of simple automations",
        "The best automations are embarrassingly simple: if-then logic",
        "Start with what annoys you most, automate the trigger not the whole process",
        "Complex AI systems often create more work than they save (60% accuracy example)",
    ],
    statistics=[
        "50+ automations built last year",
        "80% of value from simple workflows, 15% from basic AI, 5% from sophisticated AI",
        "Client spent $15,000 on AI system that worked only 60% of the time",
    ],
    contrarian_angles=[
        "Sophisticated AI agents are overrated for most business use cases",
        "Most automation value comes from boring if-then logic, not AI",
        "Complexity is a trap - simple wins",
    ],
    story_hooks=[
        "Client wanted AI email assistant - 6 weeks and $15,000 later, 60% accuracy",
        "50+ companies worked with, pattern emerged: simple wins",
    ],
    actionable_takeaways=[
        "Ask 4 questions before automating: trigger, action, frequency, failure mode",
        "Start with daily tasks (highest ROI)",
        "Review weekly, iterate monthly",
    ],
)


def create_sample_posts():
    """Create sample posts to demonstrate output structure."""
    tz = ZoneInfo("Europe/Helsinki")
    posts = []

    # Sample LinkedIn posts
    linkedin_content = [
        ("hook", """Most people think AI automation requires machine learning.

They're wrong.

After building 50+ automations last year, here's the truth:

80% of the value comes from simple if-then rules.

Not AI agents. Not ML models. Basic logic:
→ If email contains "invoice", forward to accounting
→ When doc uploaded, notify team
→ Every Friday, generate report

One client spent $15,000 on a fancy AI email system.
It worked 60% of the time.

Meanwhile, a 10-minute Zapier workflow solved their actual problem.

The automation that will 10x your productivity isn't complicated.

It's embarrassingly simple.

What's the most annoying repetitive task you do daily?

#AIAutomation #Productivity #FutureOfWork"""),
        ("story", """Last month, a client called me frustrated.

"We spent six weeks building an AI email assistant. It's a disaster."

$15,000. Multiple engineers. Sophisticated NLP.

60% accuracy.

The other 40%? It created MORE work - staff had to review and fix AI mistakes.

I asked one question: "What triggers the need for a response?"

Turns out, 80% of their emails fell into 5 categories.

In 2 hours, we built simple rules:
- Invoice → Accounting
- Support → Helpdesk
- Sales inquiry → CRM + notification

No AI. Just if-then logic.

Result? 95% accuracy. Zero supervision needed.

The lesson: Before reaching for AI, ask if simple rules will work.

They usually do.

#Automation #AI #Productivity"""),
    ]

    for i, (post_type, content) in enumerate(linkedin_content, 1):
        posts.append(SocialPost(
            platform=Platform.LINKEDIN,
            post_type=PostType.HOOK if post_type == "hook" else PostType.STORY,
            content=content,
            scheduled_date=datetime.now(tz) + timedelta(days=i),
            scheduled_time="17:00",
            day_number=i,
            source_article_url=SAMPLE_ARTICLE.url,
            source_article_title=SAMPLE_ARTICLE.title,
            hashtags=["AIAutomation", "Productivity"],
        ))

    # Sample Twitter posts
    twitter_content = [
        ("tweet", "80% of automation value comes from simple if-then rules. Not AI agents. Not ML models. Just triggers and actions. Most people overcomplicate this."),
        ("thread", None, [
            "I've built 50+ automations for companies this year. Here's the counterintuitive truth about what actually works: 🧵",
            "The biggest wins came from embarrassingly simple automations. Not AI. Not ML. Basic if-then logic.",
            "Example: Client spent $15k on AI email assistant. 60% accuracy. Meanwhile, 5 simple rules solved 80% of their problem.",
            "The 80/20 of automation:\n→ 80% of value: trigger-based workflows\n→ 15%: basic AI (summarization, categorization)\n→ 5%: sophisticated AI agents",
            "Yet most companies chase that 5%.",
            "Before building any automation, ask:\n1. What's the trigger?\n2. What's the action?\n3. How often does this happen?\n4. What if it fails?",
            "Start simple. Ship fast. Iterate.\n\nFull breakdown: https://theinterneteconomy.xyz/p/80-20-ai-automation",
        ]),
    ]

    for i, item in enumerate(twitter_content, 1):
        if item[0] == "tweet":
            posts.append(SocialPost(
                platform=Platform.TWITTER,
                post_type=PostType.TWEET,
                content=item[1],
                scheduled_date=datetime.now(tz) + timedelta(days=i),
                scheduled_time="17:00",
                day_number=i,
                source_article_url=SAMPLE_ARTICLE.url,
                source_article_title=SAMPLE_ARTICLE.title,
            ))
        else:
            posts.append(SocialPost(
                platform=Platform.TWITTER,
                post_type=PostType.THREAD,
                content="\n\n".join(item[2]),
                scheduled_date=datetime.now(tz) + timedelta(days=i),
                scheduled_time="17:00",
                day_number=i,
                source_article_url=SAMPLE_ARTICLE.url,
                source_article_title=SAMPLE_ARTICLE.title,
                thread_tweets=item[2],
            ))

    return posts


def main():
    print("=" * 70)
    print("Content Agent Demo - Prompts and Output Structure")
    print("=" * 70)

    # Show system prompt
    print("\n[1] SYSTEM PROMPT (Used for all generation)")
    print("-" * 50)
    print(SYSTEM_PROMPT[:500] + "...")

    # Show analysis prompt
    print("\n\n[2] ARTICLE ANALYSIS PROMPT")
    print("-" * 50)
    analysis_prompt = ANALYSIS_PROMPT.format(
        title=SAMPLE_ARTICLE.title,
        source=SAMPLE_ARTICLE.source_substack,
        category=SAMPLE_ARTICLE.category,
        content=SAMPLE_ARTICLE.content[:200] + "...",
    )
    print(analysis_prompt[:600] + "...")

    # Show LinkedIn hook prompt
    print("\n\n[3] LINKEDIN HOOK PROMPT (Day 1)")
    print("-" * 50)
    hook_prompt = LINKEDIN_PROMPTS["hook"].format(
        title=SAMPLE_ARTICLE.title,
        url=SAMPLE_ARTICLE.url,
        main_thesis=SAMPLE_ANALYSIS.main_thesis,
        key_points="\n".join(f"- {p}" for p in SAMPLE_ANALYSIS.key_points[:3]),
        statistics="\n".join(f"- {s}" for s in SAMPLE_ANALYSIS.statistics),
        quotes="",
        story_hooks="\n".join(f"- {h}" for h in SAMPLE_ANALYSIS.story_hooks),
        contrarian_angles="\n".join(f"- {c}" for c in SAMPLE_ANALYSIS.contrarian_angles),
        actionable_takeaways="\n".join(f"- {t}" for t in SAMPLE_ANALYSIS.actionable_takeaways),
    )
    print(hook_prompt[:800] + "...")

    # Show post schedule
    print("\n\n[4] WEEKLY POST SCHEDULE")
    print("-" * 50)
    print("\nLinkedIn:")
    for item in LINKEDIN_POST_SCHEDULE:
        print(f"  Day {item['day']}: {item['name']} ({item['type']})")
    print("\nTwitter:")
    for item in TWITTER_POST_SCHEDULE:
        print(f"  Day {item['day']}: {item['name']} ({item['type']})")

    # Create sample output
    print("\n\n[5] GENERATING SAMPLE OUTPUT FILES")
    print("-" * 50)

    posts = create_sample_posts()
    linkedin_posts = [p for p in posts if p.platform == Platform.LINKEDIN]
    twitter_posts = [p for p in posts if p.platform == Platform.TWITTER]

    week = ContentWeek(
        source_article_title=SAMPLE_ARTICLE.title,
        source_article_url=SAMPLE_ARTICLE.url,
        source_substack=SAMPLE_ARTICLE.source_substack,
        linkedin_posts=linkedin_posts,
        twitter_posts=twitter_posts,
        notes_posts=[],
    )

    # Write outputs
    markdown_writer = MarkdownWriter("./output")
    json_exporter = JSONExporter("./output")
    csv_exporter = CSVExporter("./output")

    folder_path = markdown_writer.write_week(week)
    json_exporter.export_week(week, folder_path)
    csv_exporter.export_week(week, folder_path)

    print(f"\nOutput saved to: {folder_path}")
    print("\nFiles created:")
    for f in sorted(folder_path.rglob("*")):
        if f.is_file():
            print(f"  {f.relative_to(folder_path)}")

    # Show sample LinkedIn post
    print("\n\n[6] SAMPLE LINKEDIN POST (Day 1 - Hook)")
    print("-" * 50)
    print(linkedin_posts[0].content)

    # Show sample Twitter thread
    print("\n\n[7] SAMPLE TWITTER THREAD (Day 2)")
    print("-" * 50)
    thread = twitter_posts[1]
    for i, tweet in enumerate(thread.thread_tweets, 1):
        print(f"{i}/ {tweet}\n")

    print("\n" + "=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print("\nTo use with real articles:")
    print("  1. Set ANTHROPIC_API_KEY in .env")
    print("  2. Run: content-agent generate")
    print("  3. Or: content-agent generate --url 'https://your-substack.xyz/p/article'")


if __name__ == "__main__":
    main()
