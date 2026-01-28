"""LinkedIn-specific prompt templates optimized for engagement."""

# Post schedule: which type on which day
LINKEDIN_POST_SCHEDULE = [
    {"day": 1, "type": "hook", "name": "Hook Post"},
    {"day": 2, "type": "story", "name": "Story Post"},
    {"day": 3, "type": "listicle", "name": "Listicle"},
    {"day": 4, "type": "question", "name": "Question Post"},
    {"day": 5, "type": "contrarian", "name": "Contrarian Take"},
    {"day": 6, "type": "howto", "name": "How-To/Framework"},
    {"day": 7, "type": "cta", "name": "CTA Post"},
]

LINKEDIN_PROMPTS = {
    "hook": """Create a LinkedIn post using the HOOK format that stops the scroll.

SOURCE ARTICLE:
Title: {title}
Key Points: {key_points}
Statistics: {statistics}
Main Thesis: {main_thesis}

HOOK POST FORMULA (proven to get 3x engagement):

1. OPENING LINE (THE HOOK) - First 2 lines are everything
   - Must be bold, surprising, or challenge assumptions
   - Under 12 words ideally
   - Creates an "information gap" - reader NEEDS to click "see more"
   - Examples of great hooks:
     * "Most AI tools are making you less productive."
     * "I deleted my to-do list. My output tripled."
     * "The best salespeople never sell."

2. THE GAP (2-3 lines after the fold)
   - Build curiosity without revealing the insight
   - Use phrases like "Here's what I discovered..." or "The reason is counterintuitive..."

3. THE REVEAL (3-5 short paragraphs)
   - Use single-sentence paragraphs for readability
   - Include ONE specific example, number, or data point
   - Each paragraph should be 1-2 lines max

4. THE CLOSE (1-2 lines)
   - Either a thought-provoking question OR a clear takeaway
   - No begging for engagement
   - If including a question, make it genuinely interesting

CHARACTER TARGET: 1,000-1,300 characters (sweet spot for LinkedIn)

OUTPUT FORMAT (copy exactly):
---
[Opening hook line - bold and surprising]

[Curiosity gap - 2-3 lines]

[Reveal - short paragraphs with key insight]

[Close - question or takeaway]

#Hashtag1 #Hashtag2 #Hashtag3
---

Generate the post now. Make the hook irresistible.""",

    "story": """Create a LinkedIn STORY post that builds connection through narrative.

SOURCE ARTICLE:
Title: {title}
Story Hooks: {story_hooks}
Key Points: {key_points}
Main Thesis: {main_thesis}

STORY POST FORMULA (highest save/share rate):

1. SCENE SETTING (First 2 lines - before the fold)
   - Drop the reader into a specific moment
   - Use concrete details: time, place, situation
   - Examples:
     * "Last Tuesday at 2 AM, I was debugging a client's automation."
     * "Three years ago, I was charging $50/hour."
     * "The email landed at 6 AM. Subject line: 'We need to talk.'"

2. THE CHALLENGE (What happened?)
   - What problem or unexpected situation arose?
   - Make the reader feel the tension

3. THE TURNING POINT (What changed?)
   - The moment of realization or shift
   - This should connect to the article's main insight

4. THE LESSON (The universal truth)
   - Connect your story to something the reader can apply
   - Make it about THEM, not you

5. THE TAKEAWAY (One actionable insight)
   - What can they do differently starting today?

CHARACTER TARGET: 1,200-1,500 characters

OUTPUT FORMAT:
---
[Scene setting - specific moment]

[The challenge - what went wrong or what tension arose]

[Turning point - the shift]

[The lesson - universal truth]

[Takeaway - what they can do]

#Hashtag1 #Hashtag2 #Hashtag3
---

Generate the post now. Make it feel real and specific.""",

    "listicle": """Create a LinkedIn LISTICLE post with actionable takeaways.

SOURCE ARTICLE:
Title: {title}
Key Points: {key_points}
Actionable Takeaways: {actionable_takeaways}
Main Thesis: {main_thesis}

LISTICLE FORMULA (easiest to consume, high engagement):

1. HOOK LINE (Before the fold)
   - Number + Promise
   - Examples:
     * "7 automations I wish I'd built years ago:"
     * "5 mistakes killing your LinkedIn engagement:"
     * "3 tools that replaced my entire tech stack:"

2. THE LIST (5-7 items)
   - Each item: Bold statement + 1 line of context
   - Use arrows (→) or dashes (-)
   - Keep each point scannable
   - Order from most impactful to least (or save best for last)

3. THE CLOSE
   - Quick summary or ask which one resonated most

CHARACTER TARGET: 1,000-1,400 characters

OUTPUT FORMAT:
---
[Hook: Number + Promise]

→ [Point 1]: [One line context]

→ [Point 2]: [One line context]

→ [Point 3]: [One line context]

→ [Point 4]: [One line context]

→ [Point 5]: [One line context]

[Close - summary or question]

#Hashtag1 #Hashtag2 #Hashtag3
---

Generate the post now. Make each point specific and actionable.""",

    "question": """Create a LinkedIn QUESTION post that sparks discussion.

SOURCE ARTICLE:
Title: {title}
Contrarian Angles: {contrarian_angles}
Key Points: {key_points}
Main Thesis: {main_thesis}

QUESTION POST FORMULA (drives comments and shares):

1. SETUP (2-3 lines before the question)
   - Present an observation or trend
   - Create context that makes the question meaningful
   - Example: "Everyone's talking about AI replacing jobs. But I've noticed something different..."

2. THE QUESTION (Must be thought-provoking)
   - Not yes/no - should require real thought
   - Slightly controversial is good
   - Should relate to the reader's experience
   - Examples:
     * "What's the most overrated productivity advice you've ever received?"
     * "When did you realize your industry had fundamentally changed?"

3. YOUR PERSPECTIVE (Brief)
   - Share your own answer or view (2-3 lines)
   - This invites others to agree or disagree

CHARACTER TARGET: 600-900 characters (shorter posts with questions perform well)

OUTPUT FORMAT:
---
[Setup - observation or context]

[THE QUESTION - thought-provoking, not yes/no]

[Your brief perspective]

#Hashtag1 #Hashtag2 #Hashtag3
---

Generate the post now. Make the question genuinely interesting.""",

    "contrarian": """Create a LinkedIn CONTRARIAN post that challenges conventional wisdom.

SOURCE ARTICLE:
Title: {title}
Contrarian Angles: {contrarian_angles}
Statistics: {statistics}
Main Thesis: {main_thesis}

CONTRARIAN POST FORMULA (highest share potential):

1. THE CONTRARIAN HOOK (First line)
   - State the popular belief, then flip it
   - Examples:
     * "Everyone says 'work smarter, not harder.' They're wrong."
     * "The '10x developer' is a myth. Here's what actually matters."
     * "I stopped tracking my time. My productivity increased."

2. THE COMMON WISDOM (What most people believe)
   - Acknowledge the standard advice
   - Show you understand why people believe it

3. THE FLIP (Your contrarian view)
   - Present your alternative perspective
   - Back it up with evidence, data, or experience from the article

4. THE EVIDENCE (Why your view is valid)
   - Specific examples or data
   - Real results or observations

5. THE NUANCE (Important!)
   - Acknowledge when the common wisdom IS correct
   - This makes you credible, not just contrarian for controversy's sake

CHARACTER TARGET: 1,100-1,400 characters

OUTPUT FORMAT:
---
[Contrarian hook - flip the common wisdom]

[The common wisdom - what most believe]

[The flip - your alternative view]

[The evidence - why this works]

[The nuance - when the common wisdom applies]

#Hashtag1 #Hashtag2 #Hashtag3
---

Generate the post now. Be bold but substantive.""",

    "howto": """Create a LinkedIn HOW-TO/FRAMEWORK post that provides actionable value.

SOURCE ARTICLE:
Title: {title}
Actionable Takeaways: {actionable_takeaways}
Key Points: {key_points}
Main Thesis: {main_thesis}

HOW-TO POST FORMULA (highest save rate):

1. THE PROMISE (First line)
   - Clear, specific outcome
   - Examples:
     * "How to automate 80% of your email in 30 minutes:"
     * "My 3-step framework for writing LinkedIn posts that convert:"
     * "The exact system I use to generate 10 content ideas in 5 minutes:"

2. THE CONTEXT (Why this matters - 1-2 lines)
   - Quick pain point or benefit statement

3. THE FRAMEWORK/STEPS (3-5 steps)
   - Numbered or bulleted
   - Each step is actionable and specific
   - Include the "how" not just the "what"

4. THE EXAMPLE (Optional but powerful)
   - Show one step in action

5. THE CLOSE
   - Encourage them to try it or ask which step they'll start with

CHARACTER TARGET: 1,200-1,500 characters

OUTPUT FORMAT:
---
[Promise - specific outcome]

[Context - why this matters]

Step 1: [Action + brief how]
Step 2: [Action + brief how]
Step 3: [Action + brief how]
[Optional: Step 4-5]

[Example if applicable]

[Close - encourage action]

#Hashtag1 #Hashtag2 #Hashtag3
---

Generate the post now. Make every step actionable.""",

    "cta": """Create a LinkedIn CTA post that drives readers to the full article.

SOURCE ARTICLE:
Title: {title}
URL: {url}
Key Points: {key_points}
Main Thesis: {main_thesis}

CTA POST FORMULA (drives traffic without being salesy):

1. THE HOOK (Value-first opening)
   - Start with insight, not promotion
   - Example: "I spent 40 hours researching AI automation trends. Here's what surprised me most:"

2. THE VALUE PREVIEW (3-4 key insights)
   - Give them real value in the post itself
   - Tease what's in the full article
   - Don't hold everything back - give them enough to trust you

3. THE BRIDGE
   - Natural transition to the article
   - Example: "I wrote about this in depth..." or "The full breakdown covers..."

4. THE CTA (Natural, not desperate)
   - Link naturally integrated
   - Never: "Check out my newsletter!"
   - Better: "Full breakdown with examples: [link]"

CHARACTER TARGET: 900-1,200 characters

OUTPUT FORMAT:
---
[Hook - value-first opening]

[Value preview - 3-4 key insights from the article]

[Bridge - natural transition]

Full article: {url}

#Hashtag1 #Hashtag2 #Hashtag3
---

Generate the post now. Lead with value, not promotion.""",
}
