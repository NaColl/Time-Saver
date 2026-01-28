"""Twitter/X-specific prompt templates optimized for engagement."""

# Post schedule: which type on which day
TWITTER_POST_SCHEDULE = [
    {"day": 1, "type": "tweet", "name": "Single Tweet"},
    {"day": 2, "type": "thread", "name": "Thread (5-7)"},
    {"day": 3, "type": "tweet", "name": "Hot Take Tweet"},
    {"day": 4, "type": "thread", "name": "Breakdown Thread"},
    {"day": 5, "type": "tweet", "name": "Quote/Stat Tweet"},
    {"day": 6, "type": "thread", "name": "Story Thread"},
    {"day": 7, "type": "tweet_cta", "name": "CTA Tweet"},
]

TWITTER_PROMPTS = {
    "tweet": """Create a single high-impact tweet from this article.

SOURCE ARTICLE:
Title: {title}
Key Points: {key_points}
Statistics: {statistics}
Main Thesis: {main_thesis}

SINGLE TWEET FORMULA:

Requirements:
- MUST be under 280 characters (this is critical)
- One clear, punchy insight
- No hashtags unless absolutely essential (0-1 max)
- Should work standalone - no context needed

What works on X:
- Counterintuitive observations
- Specific numbers or results
- Confident opinions (not hedged)
- Statements that make people think "I need to share this"

Examples of great tweets:
- "The best content isn't original. It's familiar ideas explained better."
- "80% of my automations are just if-then statements. Complexity is overrated."
- "I've worked with 50+ clients. The ones who succeed ship fast and iterate. The rest plan forever."

OUTPUT FORMAT:
---
[Your tweet under 280 characters]
---

Generate the tweet now. Make it quotable.""",

    "thread": """Create a Twitter thread (5-7 tweets) from this article.

SOURCE ARTICLE:
Title: {title}
Key Points: {key_points}
Story Hooks: {story_hooks}
Actionable Takeaways: {actionable_takeaways}
Main Thesis: {main_thesis}

THREAD FORMULA (optimized for engagement):

Tweet 1 (THE HOOK) - Most important tweet:
- Bold claim, surprising stat, or promise
- Must make people want to read more
- End with "A thread:" or "Here's what I learned:" or similar
- Example: "I spent 3 months building AI automations for 20 different companies. Here's what actually moved the needle (it's not what you'd expect):"

Tweets 2-5 (THE CONTENT):
- One key point per tweet
- Each tweet should work standalone if shared
- Use → or • for lists within tweets
- Include specific examples or numbers when possible
- Keep building momentum

Tweet 6 (THE SUMMARY):
- Recap the core insight
- Crystallize the main takeaway

Tweet 7 (THE CTA):
- Where to learn more (link to article)
- Natural invitation, not desperate pitch
- Example: "I wrote a full breakdown here: [link]"

RULES:
- Each tweet MUST be under 280 characters
- No hashtags in the hook tweet
- Maximum 1 hashtag in final tweet only
- Don't start tweets with "I" repeatedly
- Vary sentence structure

OUTPUT FORMAT:
---
1/ [Tweet 1 - the hook, end with thread indicator]

2/ [Tweet 2]

3/ [Tweet 3]

4/ [Tweet 4]

5/ [Tweet 5]

6/ [Tweet 6 - summary]

7/ [Tweet 7 - CTA with link: {url}]
---

Generate the thread now. Make the hook irresistible.""",

    "tweet_cta": """Create a single tweet with a call-to-action to the article.

SOURCE ARTICLE:
Title: {title}
URL: {url}
Key Points: {key_points}
Main Thesis: {main_thesis}

CTA TWEET FORMULA:

Requirements:
- Under 280 characters
- Lead with value/insight, not self-promotion
- Link naturally integrated
- No "check out my blog" energy

Good patterns:
- "I wrote about [insight]. [Link]"
- "[Key insight from article]. Full breakdown: [Link]"
- "[Question or observation]? I explored this in depth: [Link]"

OUTPUT FORMAT:
---
[Your tweet with link: {url}]
---

Generate the tweet now. Lead with value.""",
}
