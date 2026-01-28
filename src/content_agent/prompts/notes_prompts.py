"""Substack Notes-specific prompt templates."""

# Notes are more conversational, community-focused
NOTES_PROMPTS = {
    "note": """Create a Substack Note from this article.

SOURCE ARTICLE:
Title: {title}
URL: {url}
Key Points: {key_points}
Quotes: {quotes}
Main Thesis: {main_thesis}
Day Number: {day_number}

SUBSTACK NOTES CONTEXT:
- Substack Notes is more intimate than Twitter/LinkedIn
- Readers are already newsletter subscribers or interested in long-form content
- More conversational, less "performative"
- Can be longer than tweets (up to 500 words, but shorter is fine)
- Great for sharing insights, asking questions, or teasing content

DAY-BASED APPROACH:
- Day 1: Share the core insight with a fresh angle
- Day 2: Pull out an interesting quote or example
- Day 3: Ask a thought-provoking question related to the article
- Day 4: Share a "behind the scenes" or personal reflection
- Day 5: Highlight a specific actionable tip
- Day 6: Connect the article to a current trend or news
- Day 7: Invite discussion or feedback on the ideas

TONE:
- More casual than LinkedIn
- Can be more personal and reflective
- Less "optimized" feeling - more authentic
- Like talking to your reading community

OUTPUT FORMAT:
---
[Your Substack Note - 100-300 words typically]

Read the full piece: {url}
---

Generate the note now. Make it feel like a genuine thought share, not a promotional post.""",
}
